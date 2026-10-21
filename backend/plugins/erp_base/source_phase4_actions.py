"""第四阶段页面入口，资源重新生成后继续保留。"""
import json
from pathlib import Path
from .source_phase2_actions import field

FUNCTIONS=['fn_ArticlePriceWeightedAverage','fn_StuffPriceWeightedAverage','fn_ConcatJobAtte','fn_ConcatWeightKg',
 'fn_Get_JiaoDai','Fn_Get_Machine','fn_GetJObSheetNoAttePrice','fn_GetJObSheetNoAttePriceUnit','fn_GetPaperTubeByJobNo',
 'fn_GetPhaseNo','fn_GetProcessWorkMoney','fn_GetTubeWeightByJobNo','fn_JobAssign','fn_JobAttelect','fn_ProcessIDPire','fn_ProcessIDPrice','GetPropOfJobShiftEmp','F_JobProcessTable']
OPERATIONS=['Sp_JobGrayRecord_JobSheet_Update','Sp_Update_JobSheet_Structure','Sp_JobPackRemarks','sp_JobProcess_New',
 'sp_JobProcess_New1','Sp_JobProcessUpdate','Sp_JobProcessUpdate_Curr2','Up_RecordEmp','Up_RecordEmp1','UpdateJobSheet_Field','Sp_StuffIDPrice',
 'GetCustProdstandcraft','DyeUseOver_UPDTEA','Sp_UpdateJobSheetAndJobProcess','Sp_UpdateJobSheetAndJobProcessNT',
 'Sp_UpdateJobOutAC','sp_ProduseBarCode','Sp_StuffRegisterAutoOutPut']


def extend(resources):
    queries=json.loads(Path(__file__).with_name('source_phase4_queries.json').read_text(encoding='utf8'))
    texts=[('jobsheetno','工卡号'),('sheetseries','单据流水号'),('jobseries','工卡流水号'),('programid','程序编号'),
        ('processid','工序编号'),('empid','员工编号'),('wprocessno','报工号'),('shiftid','班组编号'),('customerid','客户编号'),
        ('attevalue','附加项目'),('stuffcode','染化料编号'),('articlecode','机物料编号'),('warehouseid','仓库编号'),
        ('barcode','条码'),('machineid','机台编号'),('confilter','查询内容'),('filetype','附件类型'),('machineclass','故障分类'),('model','机台型号'),
        ('sheetno','单据号'),('detailno','明细号'),('stereotypesname','预排机台'),('status','设备状态'),('businessid','工厂'),('deptid','部门'),('empgroup','维修组'),('sheetkind','单据类型')]
    common=[field(k,t) for k,t in texts]
    common.extend(field(k,t) for k,t in [('workstatus','报工状态'),('groupfields','配件汇总字段（逗号分隔）'),('machinelist','机台列表（逗号分隔，全部）'),('counttype','统计周期（月/日/年/机台）'),('handlerids','维修人员'),('postname','岗位名称'),('empids','考勤员工'),('deptids','考勤部门'),('rollno','卷号'),('strlabelrptid','标签报表'),('upsheetseries','来源流水'),('keeper','保管人'),('stationid','工位'),('driver','司机'),('receivingtype','收坯类型'),('colornum','色号'),('lotno','批号')])
    common.extend(field(k,t,'number',default=v) for k,t,v in [('dpkind','报工方式（0全程/1开始/2结束）',0),('delivery','派送类型',0),('datecount','图表天数',10),('containclosed','包含关闭故障',1),('totalmode','配件汇总方式0—8',0),('upkind','出库来源1半成品2坯料',1)])
    common.extend(field(k,t,'datetime') for k,t in [('worktime','报工时间'),('eddate','考勤结束时间'),('newstime','计件开始时间'),('newetime','计件结束时间'),('ymdate','生产统计日期')])
    common.extend(field('ischecked'+str(i),'原查询开关'+str(i),default='N') for i in range(1,7))
    common.extend(field(k,t,'number',default=v) for k,t,v in [('ischarge','附加项目模式',0),('kind','原分类',0),('processno','工序序号',0),('rounds','配件提交轮次',0),('current','页码',1),('size','每页数量',20)])
    common.extend(field(k,t,'decimal') for k,t in [('ratio','岗位系数'),('price','原单价'),('currkg','本次重量'),('num','区间数量')])
    common.extend(field(k,t,'datetime') for k,t in [('startdate','开始时间'),('enddate','结束时间')])
    common.extend(field(k,t,'datetime') for k,t in [('starttime','故障开始时间'),('endtime','故障结束时间'),('dtdate','统计日期')])
    common.extend(field(k,t,'number',default=v) for k,t,v in [('countday','统计天数',30),('aboutme','只看相关人员',0),('searchmode','原筛选模式',0),('returnmaxcount','最多返回行数（0为全部）',0)])
    for model,options in resources.items():
        if model in ['SourceDyeWProcess','SourceDyeKQ','SourceDyeKQQuery','SourceDyeEmpShiftClock','SourceDyeDPWorkQty']:
            options['workflow']['actions'].append({'key':'phase4_attendance','title':'原考勤及包装计件重算（原行留档）','detail':False,'inputs':[
                field('name','办理项目','select',required=True,options=[{'value':n,'label':n} for n in ['qry_Static_EmpTotal','sp_EmpID_CHECK_Query','sp_EmpID_CHECKINOUT','sp_Static_Emp','sp_DPWorkQty_Query']]),
                field('dtdate','开始日期','datetime',required=True),field('eddate','结束日期','datetime',required=True),field('empids','员工'),field('deptids','部门')]})
        if model in ['SourceDyeMachineFault','SourceDyeGetClothNotice','SourceDyeMachineFaultArticleInfo','SourceDyeAPPUploadFilesInfo']:
            options['workflow']['actions'].append({'key':'phase4_equipment','title':'收坯通知、维修配件及附件原保存','detail':False,'inputs':[
                field('name','办理项目','select',required=True,options=[{'value':n,'label':n} for n in ['Sp_APP_CheckGetClothNotice','Sp_APP_SaveGetClothNotice','sp_App_SaveFaultArticleListBySheetSeries','sp_App_SaveMachineArticleBill','sp_App_SaveMachineDeliverBill','sp_App_SaveUploadFilesInfo']]),
                *[field(k,t) for k,t in [('sheetseries','单据流水'),('upsheetseries','待修改通知流水'),('driver','司机'),('licenseplate','车牌'),('empid','员工'),('remarks','备注'),
                    ('customeridlist','客户列表（逗号分隔）'),('addrdlvlist','地址列表（逗号分隔）'),('prodidlist','布种列表（逗号分隔）'),('rollslist','条数列表（逗号分隔）'),('clothgetdetailnolist','原收坯明细列表（逗号分隔）'),
                    ('serialnumlist','序号列表（分号分隔）'),('articleidlist','配件编号列表（分号分隔）'),('articlenamelist','配件名称列表（分号分隔）'),('speclist','规格列表（分号分隔）'),('qtylist','数量列表（分号分隔）'),('kindlist','分类列表（分号分隔）'),
                    ('articleid','配件编号'),('qty','配件数量'),('unit','单位'),('resultid','维修结果'),('handleidea','处理意见'),('handlerids','维修工号列表'),
                    ('guid','附件原Guid'),('orifilename','原文件名'),('savefilename','保存文件名'),('filenameurl','附件地址'),('userid','录入人')]],
                field('delivery','派送1/办理0','number',default=0),field('kind','附件分类','number',default=0),field('uiindex','附件顺序','number',default=0),field('savedate','附件日期','datetime')]})
        if model not in ['SourceDyeJobSheet','SourceDyeStuffWeight','SourceDyeWProcess','SourceDyeMachineFault','SourceDyeRecordYield','SourceDyePStuff']:continue
        actions=options['workflow']['actions']
        for key,title,names in [('phase4_report','生产、称料和设备原查询',queries),('phase4_function','工卡及工序原函数',FUNCTIONS),('phase4_operation','工卡和包装人员原办理',OPERATIONS)]:
            actions.append({'key':key,'title':title,'detail':False,'inputs':[
                field('name','办理项目','select',required=True,options=[{'value':n,'label':n} for n in names]),*common,
                *([field('machine_programs','现场中控程序对应','editable_rows',default=[],columns=[field(n,n) for n in ['ProgNo','ProgId','MachineId']])] if key=='phase4_report' else [])]})
