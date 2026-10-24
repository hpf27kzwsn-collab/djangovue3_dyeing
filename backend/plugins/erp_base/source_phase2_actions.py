"""销售/打样第二阶段页面动作配置；生成模型资源时同样保留。"""
import json
from pathlib import Path


def field(key,title,kind='text',**extra):
    return {'key':key,'title':title,'kind':kind,'required':False,'nullable':True,'options':[],**extra}


def extend(resources):
    query_names=json.loads(Path(__file__).with_name('source_phase2_queries.json').read_text(encoding='utf8'))
    for model,options in resources.items():
        actions=options['workflow']['actions']
        if model in ['SourceDyeOrderMain','SourceDyeQuote','SourceDyeDyeDipsRecord','SourceDyeSampleStockBook']:
            actions.append({'key':'phase2_report','title':'订单、报价与小样完整查询','detail':False,'inputs':[
                field('name','查询项目','select',required=True,options=[{'value':n,'label':spec['title']} for n,spec in query_names.items()]),
                field('startdate','开始日期','date'),field('enddate','结束日期','date'),field('confilter','查询内容'),
                field('customerid','客户编号'),field('sheetseries','订单流水号'),field('sheetno','订单号'),field('prodid','品种编号'),
                field('fabrickind','品种类别'),field('colordepthid','色级'),field('empid','员工编号'),
                field('bisaccept','仅待接收','boolean',default=False),field('current','页码','number',default=1),field('size','每页数量','number',default=20)]})
        if model in ['SourceDyeQuote','SourceDyeFixedPrice','SourceDyeDyeDipsRecord']:
            actions.append({'key':'phase2_price','title':'核对配方及客户单价','detail':False,'inputs':[
                field('name','计算内容','select',required=True,options=[{'value':k,'label':v} for k,v in [
                    ('fn_A_GetRemarks','标签仓库及备注'),('fn_RKL','销售限制历史余额'),('Sp_ProduceColorNum','采用输入色号'),('fn_GetDyeStuffDosage','配方成本/染料用量'),('fn_GetFlowSheetInfo','订单客户及业务员'),('fn_MaterialPriceAdjust','前次材料单价'),
                    ('fn_FARMainPrice','客户确价/分头价/最低消费'),('Sp_QueryColorNumPrice','客户色号报价'),('Sp_QueryColorNum_BasicsPrice','客户基础色号价')]]),
                *[field(k,t) for k,t in [('color','色号'),('series','单据流水号'),('supplier','供应商'),('material','材料编号'),('check','订单明细号'),
                    ('job','工卡号'),('customer','客户编号'),('product','品种编号'),('category','纱线类别'),('grade','等级'),('level','色级'),('colorinput','输入色号'),('flow','原流程编号')]],
                field('kind','原计算类别','number',default=0),field('at','比较日期','datetime')]})
        if model=='SourceDyeOrderMain':
            inputs=[field(k,t) for k,t in [('DetailCustName','明细客户'),('CustSelfNo','客户单号'),('ContractNo','客户款号'),('CustomerIDMain','客户编号'),('EmpID','操作员工编号')]]
            inputs += [field('AssignUnit','原下单单位编号','number',default=-1),
                field('details','颜色及数量明细','editable_rows',default=[],columns=[field(k,t,kind) for k,t,kind in [
                    ('ColorID','颜色','text'),('ColorNum','染厂色号','text'),('CustColorNum','客户色号','text'),('CustFabricName','客户品名','text'),
                    ('CustSelfProduct','客户缸号','text'),('LotNo','成份','text'),('DlvDate','发货日期','datetime'),('OrderQty','重量','decimal'),('OrderRolls','匹数','decimal')]]),
                field('requirements','加工要求','editable_rows',default=[],columns=[field(k,t) for k,t in [('AtteCode','要求编码'),('AtteValue','事项内容'),('Description','描述'),('FieldType','要求类别')]])]
            for key,title,detail in [('app_order_save','按现场订单方式录入',False),('app_order_modify','替换订单并保留旧版',True)]:
                actions.append({'key':key,'title':title,'detail':detail,'states':['unreviewed', 'approved', None],'inputs':inputs})
            actions.extend([
                {'key':'app_order_check','title':'检查原订单修改状态','states':['unreviewed', 'approved', None],'inputs':[]},
                {'key':'refresh_order_prices','title':'回写订单收费单价','states':['unreviewed', 'approved', None],'inputs':[field('feel_only','仅手感要求','boolean',default=False),field('all_orders','全部订单手感收费','boolean',default=False)]}])
        if model=='SourceDyeDyeReprint':actions.append({'key':'reprint_allocation','title':'按复版人员分配产量','states':['unreviewed', 'approved', None],'inputs':[]})
        if model in ['SourceDyeStuffIn','SourceDyeArticleIn']:actions.append({'key':'material_price_adjustment','title':'生成材料涨价调整','states':['unreviewed', 'approved', None],'inputs':[]})
        if model=='SourceDyeSmpPrescriptEntry':actions.append({'key':'complete_sample_phases','title':'补排旧配方空阶段号','detail':False,'inputs':[]})

        if model=='SourceDyeDyeRecipe':actions.append({'key':'refresh_recipe_costs','title':'重算全部配方原连接成本','detail':False,'inputs':[]})
        if model=='SourceDyePriceAdjust':actions.append({'key':'original_quote_adjustment','title':'按原调价规则回写报价','states':['unreviewed', 'approved', None],'inputs':[field('audited','采用调价（关闭为反调价）','boolean',default=True)]})
        if model in ['SourceDyeSampleIn','SourceDyeSampleOut','SourceDyeSampleStockBook']:
            actions.append({'key':'refresh_sample_book','title':'按原明细号同步小样收发','states':['unreviewed', 'approved', None],'inputs':[
                field('sheet_no','原单据号',required=True),field('detail_no','原明细号',required=True),field('kind','收发类别','select',required=True,options=[{'value':1,'label':'入库'},{'value':2,'label':'出库'}])]})
