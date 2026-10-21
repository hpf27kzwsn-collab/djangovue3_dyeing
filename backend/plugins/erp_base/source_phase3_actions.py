"""第三阶段页面动作和原字段参数；生成资源时同样保留。"""
from .source_phase2_actions import field
import json
from pathlib import Path
QUERIES=json.loads(Path(__file__).with_name('source_phase3_queries.json').read_text(encoding='utf8'))
SPECS=json.loads(Path(__file__).with_name('source_phase3_carry.json').read_text(encoding='utf8'))
OPERATIONS=[('sp_AuTo_GrayIn','批量坯料入库'),('sp_AuTo_ProdIn_to','暂存成品入库'),('Sp_InProdInRecord','成品细码长度及坯重分摊'),
 ('Sp_InSertGrayOutRecord','工卡坯料细码分配'),('Sp_InSertSemiOutRecord','半成品出库细码重分配'),
 ('Sp_GrayOutTurn_SemiStockBook','坯料出库转半成品入库'),('Sp_SemiOutTurn_GrayStockBook','半成品出库转坯料入库'),
 ('Sp_ProdSemiOutStockInfo','坯料入库生成半成品出库'),('Sp_TurnGrayOutStockInfo','半成品入库生成坯料出库'),
 ('InToGrayPostionUp','坯料库位合并'),('InToSemiPostionUp','半成品库位合并'),('Dyeingliaodan','生成染料单'),('Dyeingliaodaninto','撤回未审核染料单'),
 ('Sp_AUTO_GrayOut','工卡坯料自动出库'),('Sp_AUTO_GrayOut_all','全部符合原条件工卡自动出库'),('Sp_AUTO_StuffAllot','执行旧自动调拨调用'),
 ('Sp_AUTO_StuffOut','近24小时实称自动出库'),('Sp_AUTO_StuffOut_small','工卡小仓自动领料'),('Sp_StuffAutoOutPutFig','计划配方自动出库'),
 ('Sp_Stuffin_Price','材料最新采购价回写'),('Sp_StuffPrice','库存流水补价'),('ToGrayBalance','出库余料自动平账'),
 ('Sp_UpdateGrayStockBook_old','旧版坯料库存保存、审核、反审核'),('UpdateSemiStock','旧版半成品明细库存'),
 ('Sp_UpdateJobSheetByProdIn','成品入库回写工卡完成状态'),('sp_zhenzhiribaobiao','保存针织日报快照'),
 *[('Sp_Update'+family+'StockBook',title+'库存办理') for family,title in [('Article','机物料'),('Gray','坯料'),('Prod','成品'),('Semi','半成品'),('Stuff','染化料')]]]


def extend(resources):
    for model,options in resources.items():
        actions=options['workflow']['actions']
        if model in ['SourceDyeGrayIn','SourceDyeGrayOut','SourceDyeSemiIn','SourceDyeSemiOut','SourceDyeStuffOut','SourceDyeProdIn',
            'SourceDyeArticleIn','SourceDyeArticleOut','SourceDyePurMain','SourceDyeSemiOutWorkApply']:
            actions.append({'key':'phase3_operation','title':'原收发、转仓及库存办理','detail':False,'inputs':[
                field('name','办理项目','select',required=True,options=[{'value':n,'label':t} for n,t in OPERATIONS]),
                field('sheetseries','来源单据流水号'),field('jobsheetseries','工卡流水号'),field('jobsheetno','工卡号'),field('entry','原库存入口名称'),
                field('state','生成方式','select',default=1,options=[{'value':1,'label':'新生成'},{'value':2,'label':'重办并保留原单'}]),
                field('updateaction','旧版库存动作','select',default=0,options=[{'value':0,'label':'保存'},{'value':1,'label':'审核'},{'value':2,'label':'反审核'}]),
                field('bookkind','旧版半成品收发','select',default=1,options=[{'value':1,'label':'入库'},{'value':2,'label':'出库'}]),
                field('staging_rows','批量坯料入库原始行','editable_rows',default=[],columns=[
                    *[field(k,t) for k,t in [('SheetSeries','单据流水'),('CustomerID','客户编号'),('GrayID','坯料编号'),('CustJobNo','客户单号'),
                        ('PreField1','预留1'),('MachineID','机台'),('PreField3','预留3'),('PreField5','预留5'),('Area','区域'),
                        ('StorageUnitIDs','库位'),('GUnit','单位'),('RollNo','卷号'),('BarCode','条码')]],field('SheetDate','日期','datetime'),
                    *[field(k,t,'decimal') for k,t in [('Rolls','匹数'),('WeightQty','重量'),('LengthQty','长度')]]])]})
        if model in ['SourceDyePurMain','SourceDyeSemiOutWorkApply','SourceDyeGrayStockBook','SourceDyeSemiStockBook',
            'SourceDyeArticleStockBook','SourceDyeStuffStockBook','SourceDyeProdStockBook']:
            actions.append({'key':'phase3_report','title':'采购、外协和库存原查询','detail':False,'inputs':[
                field('name','查询项目','select',required=True,options=[{'value':n,'label':s['title']} for n,s in QUERIES.items()]+[
                    {'value':'fn_GetEmpID','label':'工卡包装员工姓名'},{'value':'QueryQC_NewRecordInfo','label':'质检条码对应包装来源'},
                    {'value':'Sp_GrayStockToJobOut','label':'坯料条码领用查询'},{'value':'Sp_SemiStockToJobOut','label':'半成品条码领用查询'}]),
                field('startdate','开始时间','datetime'),field('enddate','结束时间','datetime'),field('ymdate','统计日期','datetime'),
                *[field(k,t) for k,t in [('customerid','客户编号'),('supplierid','供应商编号'),('grayid','坯料编号'),('prodid','品种编号'),('lotno','批号'),
                    ('recesheetno','收料明细号'),('jobsheetno','工卡号'),('sheetseries','单据流水号'),('sheetno','单据号'),('rowllno','卷号'),
                    ('stuffid','染化料编号'),('stuffcode','染化料均价编号'),('articlecode','机物料均价编号'),('articleid','机物料编号'),
                    ('articlekindid','机物料类别'),('warehouseid','仓库编号'),('prodname','品名'),('colornum','色号'),('confilter','搜索内容'),
                    ('nlotno','库存打印批号'),('fathergrayid','上级坯料编号'),('barcode','条码'),('machineid','机台编号')]],
                field('dtinputdate','计价截止时间','datetime'),field('dtinputenddate','计价起始时间','datetime'),
                *[field(f'ischecked{i}',t,'select',default='N',options=[{'value':'N','label':'不筛选'},{'value':'Y','label':'筛选'}])
                    for i,t in enumerate(['按打印批号','按客户','按品种','按起始时间','按截止时间','按仓库'],1)],
                field('current','页码','number',default=1),field('size','每页数量','number',default=20)]})
        if model in ['SourceDyeGrayStock','SourceDyeSemiStock','SourceDyeProdStock','SourceDyeStuffStock','SourceDyeArticleStock']:
            actions.append({'key':'phase3_carry','title':'原库存结转及反结转','detail':False,'inputs':[
                field('name','结转规则','select',required=True,options=[{'value':n,'label':n} for n in SPECS]),
                field('kind','办理方式','select',required=True,options=[{'value':0,'label':'结转'},{'value':1,'label':'反结转并保留原行'}]),
                field('maxstockdate','原结存时点','datetime',required=True),field('startdate','期间起点','datetime',required=True),
                field('enddate','结转时点','datetime',required=True)]})
