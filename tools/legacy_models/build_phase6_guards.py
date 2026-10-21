"""把已逐条核对的原界面条件登记为只读关系式；不运行原配置SQL。"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from sqlglot import exp,parse_one

ROOT=Path(__file__).resolve().parents[2]


def build(hooks):
    specs={}
    def register(indices,conditions,mode='last',cursor=None):
        for index in indices:
            original=hooks[index]['sql']
            match=re.search(r'cursor\s+for\s+(select.*?)\s+open\s+mycursor',original,re.I|re.S)
            variables=re.search(r'fetch\s+next\s+from\s+mycursor\s+into\s+(@\w+(?:\s*,\s*@\w+)*)',original,re.I)
            tree=parse_one(cursor or match[1],read='tsql')
            names=re.findall(r'@(\w+)',variables[1]) if variables else [e.alias_or_name for e in tree.expressions]
            assert len(names)==len(tree.expressions),(index,names)
            tree.set('expressions',[exp.alias_(e.copy(),name) for e,name in zip(tree.expressions,names)])
            # 原游标大多数没有ORDER BY；新系统明确按游标全部输出列升序，重复行不去重。
            order=tree.args.pop('order',None)
            if order:
                aliases={e.this.sql(dialect='tsql').lower():e.alias for e in tree.expressions}
                for col in order.find_all(exp.Column):col.replace(exp.column(aliases[col.sql(dialect='tsql').lower()],table='c'))
                ordering=order.sql(dialect='tsql')
            else:ordering='ORDER BY '+','.join('c.['+n+']' for n in names)
            def scope(sql):
                expression=parse_one(sql,read='tsql')
                for node in list(expression.find_all(exp.Parameter)):
                    if node.name.lower() in {n.lower() for n in names}:node.replace(exp.column(node.name,table='c'))
                return expression.sql(dialect='tsql')
            cases=' '.join('WHEN '+scope(condition)+' THEN '+scope(message) for condition,message in conditions)
            query=f"SELECT c.*,CASE {cases} ELSE NULL END AS original_message FROM ({tree.sql(dialect='tsql')}) c {ordering}"
            specs[str(index)]={'bindings':hooks[index]['entries'],'sql':query,'mode':mode,
                'original_sha256':hashlib.sha256(original.encode()).hexdigest(),'cursor_order':'original' if order else 'all_projected_columns_ascending'}
    def exists(table,where):return f'EXISTS(SELECT 1 FROM dye.{table} WHERE {where})'
    weighted=exists('StuffWeightDetail','SheetSeries=@SheetSeries1 AND ISNULL(RealQty,0)>0')
    register([0,77],[('ISNULL(@SheetStatus,0)=9',"N'料单已作废，不能修改'"),(weighted,"N'料单已经称料，不能修改'")])
    register([1,3],[(exists('StuffOut','WeightSheetNo=@SheetNo'),"N'称料单已经领料，不能删除'")])
    register([78,138],[(weighted,"N'料单已经称料，不能修改或删除'")])
    for ids,table in [([8,9],'ArticleInDetail'),([133,134],'StuffInDetail')]:
        register(ids,[(exists(table,'PurDetailNo=@DetailNo'),"N'采购申请明细已经采购入库'")])
    register([10],[(exists('SemiOutDetail','JobSheetNo=@JobSheetNo'),"N'提料缸号已半成品出库，不能删除'")],mode='any')
    register([11],[('1=1',"N'当前成本入口不能删除规格编码'")])
    for ids,table in [([13,14,15],'CusAddPrice'),([141,142,143],'ZDAddPrice')]:
        # 原ROW_NUMBER同日期无次级排序；按流水号补明确顺序，全部同号候选仍参加。
        condition=f"EXISTS(SELECT 1 FROM (SELECT SheetSeries,ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY SheetDate DESC,SheetSeries DESC) AS Num FROM dye.{table}) r WHERE r.SheetSeries=@SheetSeries AND Num>1)"
        register(ids,[(condition,"N'客户加工单价历史单据不能修改、删除或反审'")])
    register([23],[('1=1',"N'当前入库明细调整界面不能删除'")])
    register([31],[(exists('GrayInDetail','GrayApplyNo=@DetailNo'),"N'该退货申请已经退货出库，不能反审'")])
    for ids,table in [([32,33,34,35],'GrayStockAdjust'),([119,120,121,122],'SemiStockAdjust')]:
        register(ids,[(exists(table,'SheetSeries=@SheetSeries AND SheetDate<DATEADD(MONTH,-1,@ActionTime)'),"N'调整单据日期超过一个月，不能办理此动作'")])
    register([40,41],[(exists('JobOutWareEdit','InWareSheetNo=@SheetNo'),"N'进仓单已经出库，不能修改或删除'")])
    register([42],[('(SELECT COUNT(*) FROM dye.ProdIn WHERE JobSheetNo=@JobSheetNo)<0',"N'工卡已有成品入库'")])
    register([43],[(exists('SemiOutDetail','JobSheetNo=@JobSheetNo'),"N'工卡已经半成品出库'"),
        (exists('JobSheet',"ISNULL(OriSourceJobNo,'')=@JobSheetNo"),"N'工卡已经拆卡或返修'"),
        (exists('CarryMaterialDetail','JobSheetNo=@JobSheetNo'),"N'工卡已经提料'")])
    register([44,49],[("EXISTS(SELECT 1 FROM dye.GrayInDetail a JOIN dye.GrayIn b ON a.SheetSeries=b.SheetSeries WHERE b.SheetKind=14 AND a.OriJobsheetNo=@JobSheetNo)","N'工卡已车间退用到仓库，不能反中止'")])
    register([46,51],[('1=1',"N'当前查询界面不能删除业务原记录'")])
    register([47],[(exists('ProdOutDetail','JobSheetNo=@JobSheetNo'),"N'工卡已经成品出库，不能修改'")])
    register([48,115],[(exists('GrayOutDetail','JobSheetNo=@JobSheetNo'),"N'工卡已经坯布出库，不能删除'"),
        ("(CHARINDEX('C',@JobSheetNo)>0 OR CHARINDEX('H',@JobSheetNo)>0) AND @Qty>0 AND @Weight>0","N'工卡已经拆分或返修，不能删除'")])
    register([52],[('1=1',"N'原复板入口不能删除'")],cursor='SELECT 1 AS present')
    register([56],[(exists('JobCombineOrder','CheckNo=@CheckNo AND OrderSheetNo=@OrderSheetNo'),"N'订单已经合单开卡，不能删除'")],mode='any')
    register([57,75],[(exists('JobSheet','CheckNo=@CheckNo AND OrderSheetNo=@OrderSheetNo'),"N'订单已经开卡，不能修改或删除'")],mode='any')
    register([58],[(exists('JobSheet','CheckNo=@CheckNo AND OrderSheetNo=@OrderSheetNo'),"N'订单已经开卡，不能删除'")])
    register([60],[(exists('RecordYield','OutPlanSheetNo=@SheetNo'),"N'发货通知单已经扫描，不能删除'")],cursor='SELECT SheetNo FROM dye.OutPlan WHERE SheetSeries=@SheetSeries')
    register([61],[(exists('RecordYield','OutPlanDetailNo=@DetailNo'),"N'发货通知明细已经扫描，不能删除'")],cursor='SELECT @DetailNo AS DetailNo')
    register([62],[("EXISTS(SELECT 1 FROM dye.GrayOut a JOIN dye.GrayOutDetail b ON a.SheetSeries=b.SheetSeries WHERE b.JobSheetNo=@DetailNo)","N'外协加工单已经发外出库，不能删除'")])
    register([63,64],[(exists('ArticleInDetail','ArticleID=@ArticleID'),"N'机物料已经入库'"),(exists('PurApplyDetail','ArticleID=@ArticleID'),"N'机物料已经采购申请'")])
    register([65],[(exists('CookInDetail','CookID=@JobSheetNo'),"N'器具已经入库，不能删除'")],
        cursor='SELECT CookID FROM dye.p_Cook WHERE CookID=@CookID')
    register([66],[('@RightStatus=10',"N'客户已经审核，不能修改'")])
    register([68],[(exists('GrayInDetail','GrayID=@JobSheetNo'),"N'坯纱规格已经入库，不能删除'")])
    register([70],[("(SELECT COUNT(EmpID) FROM dye.p_ShiftEmp WHERE ShiftID=@ShiftID)>0","N'班组仍有员工信息，不能删除'")],cursor='SELECT @ShiftID AS ShiftID')
    register([73],[('0>0',"N'原固定为零条件，不产生拦截'")])
    for ids,back in [([81,82,85,86],True),([83,84],False)]:
        conditions=[("@SheetKind<>16 AND "+exists('ProdOutDetail','JobSheetNo=@JobSheetNo AND InSheetNo=@SheetNo'),"N'成品入库单已经出库'")]
        if back:conditions.append(("@SheetKind<>16 AND "+exists('ProdIn','JobSheetNo=@JobSheetNo AND ProdInOriSheetNo=@SheetNo'),"N'成品入库单已经退车间回修'"))
        register(ids,conditions)
    register([89,90],[(exists('ProdLoadingDetail','JobSheetNo=@JobSheetNo AND OutDetailNo=@OutDetailNo'),"N'成品出库明细已经装车'")])
    register([93],[("@SheetKind<>16 AND "+exists('JobAssign','ReceSheetNo=@ReceSheetNo'),"N'坯料批号已经开卡预配'"),
        ("@SheetKind<>16 AND "+exists('GrayOutDetail','ReceSheetNo=@ReceSheetNo'),"N'坯料批号已经出库'"),
        ("@SheetKind<>16 AND "+exists('GrayInDetail','OriReceSheetNo=@ReceSheetNo'),"N'坯料批号已经退库'"),
        ("(@SheetKind=16 OR @SheetKind IS NULL) AND EXISTS(SELECT 1 FROM dye.GrayReturnApplyDetail a WHERE a.ReceSheetNo=@OriReceSheetNo AND NOT EXISTS(SELECT 1 FROM dye.GrayInDetail b WHERE a.DetailNo=b.GrayApplyNo))","N'存在尚未退货出库的申请，不能删除当前退货单'")])
    register([94,95],[(exists('GrayInDetail','PurchaseOrders=@DetailNo'),"N'采购明细已经采购入库'")],mode='any')
    register([99,100],[('1=1',"N'该旧查询入口不允许删除已排单记录'")])
    register([130,131,132],[('@SheetKind=24',"N'调拨出库单不能修改、删除或反审'")])
    register([137],[(exists('OrderMain','CustomerID=@CustomerID1'),"N'客户已用于订单，不能删除'")])
    register([139],[(exists('JobSheet','LossStr=@SheetNo'),"N'质量评审单已经开回修卡，不能删除'")])
    register([140],[(exists('ProdInRecord','ProdBarCode=@BarCode'),"N'包装条码已成品入库，不能删除'")])
    for ids,table,kind in [([5,6,7],'Article',30),([127,128,129],'Stuff',40)]:
        used=f"EXISTS(SELECT 1 FROM dye.{table}OutDetail o LEFT JOIN dye.{table}Out h ON h.SheetSeries=o.SheetSeries LEFT JOIN dye.{table}InDetail i ON i.DetailNo=o.InDetailNo WHERE i.SheetSeries=@SheetSeries"+(' AND h.WareHouseID=12' if table=='Stuff' else '')+')'
        conditions=[('@SheetKind=15',"N'调拨入库单不能修改、删除或反审'")] if table=='Stuff' else []
        register(ids,[*conditions,(used,"N'入库单明细已经出库'")])
        for index in ids:specs[str(index)]['deferred_finance']='原FAPMain/FAPDetail转应付判断属本期暂缓财务分支；非财务收发引用仍执行'
    register([67],[(exists('JobSheet','CustomerID=@CustomerID'),"N'客户已用于工卡'"),
        (exists('GrayIn','CustomerID=@CustomerID'),"N'客户已用于坯料入库'"),(exists('FARMain','CustomerID=@CustomerID'),"N'客户已有原应收引用'")])
    register([87,88],[(exists('FARDetail','JobSheetNo=@JobSheetNo AND OutDetailNo=@OutDetailNo'),"N'装车明细已经转应收'")])
    register([76],[(exists('WProcess','JobSheetNo=@JobSheetNo')+" AND @EmpID<>'Admin'","N'缸号已登记产量，不能删除排产'")])
    register([104,105],[('@EmpID<>@DesigneeID',"N'只有单据指定审核人可以审核或反审'")])
    person="(SELECT TOP 1 Name FROM dye.h_Employee WHERE EmpID=@EmpID ORDER BY Name DESC)"
    register([113],[(person+'=@Creater',"N'不能审核自己创建的调整单据'"),(person+'=@Modifyer',"N'不能审核自己修改的调整单据'")])
    shift="(SELECT TOP 1 b.ClassID FROM dye.p_ShiftEmp a LEFT JOIN dye.p_Shift b ON a.ShiftID=b.ShiftID WHERE @ActionTime>=b.StratDate AND @ActionTime<=b.EndDate AND b.StationID='09' AND a.EmpID=@EmpID ORDER BY b.ClassID,b.ShiftID)"
    night='(DATEPART(HOUR,CAST(@ActionTime AS DATETIME))<8 OR DATEPART(HOUR,CAST(@ActionTime AS DATETIME))>=20)'
    register([53],[(f"ISNULL({shift},'')=''","N'登录人没有排班，不能审核'"),
        (f"{shift}='04' AND NOT {night}","N'当前时间为白班，登录人排夜班，不能审核'"),
        (f"{shift}<>'04' AND {night}","N'当前时间为夜班，登录人排白班，不能审核'")],cursor='SELECT 1 AS present')
    register([59],[("NOT EXISTS(SELECT 1 FROM dye.P_ColorNum p WHERE dye.F_Get_No(p.ColorNum)=dye.F_Get_No(@ColorNum) AND p.ProdID=@ProdID)","N'下单色号、布种与化验室打样资料不对应'")])
    register([136],[(exists('ProdIn','JobSheetNo=@JobSheetNo'),"N'特殊坯料出库的工卡已经成品入库'"),
        (exists('JobSheet','OriSourceJobNo=@JobSheetNo'),"N'特殊坯料出库的工卡已经拆卡或返修'")])
    register([71],[("(SELECT COUNT(EmpID) FROM dye.p_ShiftEmp WHERE ShiftID=@ShiftID)>0","N'班组仍有员工信息，不能删除'")],cursor='SELECT @ShiftID AS ShiftID')
    specs['71']['reconstruction']='原正文只有dechare；按同表其余三个班组入口的明确员工引用规则实现，不能认作原文等价'
    register([106],[("EXISTS(SELECT 1 FROM dye.p_FieldValidSub s LEFT JOIN dye.p_FieldValid f ON s.FieldType=f.FieldType AND s.Code=f.Code WHERE s.FieldType='AtteKind' AND f.Code=@Code AND EXISTS(SELECT 1 FROM dye.OrderAtte a WHERE a.AtteCode=s.SubCode))","N'加工要求子类型已经用于订单；原返回码仍为1'")],cursor='SELECT @Code AS Code')
    specs['106']['advisory']=True
    return specs


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--hooks',type=Path)
    args=parser.parse_args()
    if args.hooks:hooks=json.loads(args.hooks.read_text(encoding='utf8'))
    else:
        report=json.loads((ROOT/'docs/erp-phase6-hook-review-20261016.json').read_text(encoding='utf8'))
        hooks={}
        for row in report['bindings']:
            index=row['definition_index']
            if index not in hooks:hooks[index]={'sql':row['sql'],'entries':[]}
            assert hooks[index]['sql']==row['sql']
            hooks[index]['entries'].append([row['entry'],row['event']])
    specs=build(hooks)
    target=ROOT/'backend/plugins/erp_base/source_phase6_guards.json'
    target.write_text(json.dumps(specs,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print({'bodies':len(specs),'bindings':sum(len(v['bindings']) for v in specs.values())})
