"""质量包装交付原入口的页面配置，生成器与页面使用同一份定义。"""
import json
from pathlib import Path
from .source_phase2_actions import field

FUNCTIONS=['fn_CombineSheetNos','fn_ProdOutPriceAtte','GetRecordDefect','get_fsplit_CombineSheetNos']
OPERATIONS=['AddDeleteJobAtte','Sp_App_CheckClothGetMoney','Sp_App_SaveClothGetMoney',
 'Sp_APP_DeleteClothGetMoney','Sp_APP_DeleteGetClothNotice','SP_APP_LoadingConCloth',
 'sp_App_DeleteFaultArticleListBySheetSeries','sp_App_DeleteUploadFile','sp_AuTo_Stuff_Cancel',
 'Sp_GrayOutTurn_Delete','Sp_SemiOutTurn_Delete','SP_UpdateLinkNoCancel','sp_FuncNoPrint_delete',
 'Sp_Delete_AccessLog','s_TimerJob_Delete','Sp_StuffOutAndStockDelete','phase5_retire','phase5_undo']


def extend(resources):
    queries=json.loads(Path(__file__).with_name('source_phase5_queries.json').read_text(encoding='utf8'))
    texts=[('sheetseries','原流水号'),('upsheetseries','修改前流水号'),('jobsheetno','工卡号（自动入库撤销传流水号）'),('customerid','客户'),
      ('addrdlv','收货地址'),('empid','操作人工号'),('remarks','备注'),('prodidlist','布种列表，逗号分隔'),('rollslist','条数列表，逗号分隔'),
      ('detailno','原明细号'),('updetailnolist','通知明细号列表'),('receivingrollslist','实收条数列表'),('rowllslist','原通知条数列表'),
      ('clothgetdetailnolist','收坯申请明细号列表'),('addrdlvlist','地址列表'),('serialnumlist','配件序号列表，分号分隔'),('guid','附件Guid'),
      ('tablename1','撤销关联的第一原表'),('tablename2','撤销关联的第二原表'),('linkno','原关联号'),('itemid','调度项目号'),
      ('operation_id','本次办理编号'),('table','留档逆向的原表名'),('barcode','条码'),('text','待分拆合卡号'),('separator','分隔符'),
      ('confilter','查找内容'),('driver','司机'),('prodid','规格编号'),('colornum','色号'),('colormatching','对色员工号或合计汇总'),('classid','班次'),('shiftid','班组')]
    common=[field(k,t) for k,t in texts]+[field(k,t,'number',default=v) for k,t,v in [
       ('ischarge','收费项目1/加工项目0',0),('current','页号',1),('size','每页条数',20),('searchmode','已装车1/全部送货2',2),('context_id','办理事实编号',0),('record_id','新系统原行编号',0)]]
    common += [field(k,t,'datetime') for k,t in [('startdate','开始日期'),('enddate','截止日期'),('newstime','统计开始时间'),('newetime','统计结束时间')]]
    for model,options in resources.items():
        if model not in ['SourceDyeJobSheet','SourceDyeRecordYield','SourceDyeProdOut','SourceDyeClothGetMoney','SourceDyeGetClothNotice','SourceDyeDyeCheckout','SourceDyeZRevisionKey']:continue
        for action,title,names in [('phase5_report','质量包装交付原查询',list(queries)+['SP_ProdOutCheck']),('phase5_function','包装交付原函数',FUNCTIONS),('phase5_operation','收坯交付及原行逆向',OPERATIONS)]:
            options['workflow']['actions'].append({'key':action,'title':title,'detail':False,'inputs':[
               field('name','办理项目','select',required=True,options=[{'value':n,'label':n} for n in names]),*common]})
