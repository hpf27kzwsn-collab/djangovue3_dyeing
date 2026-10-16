"""基础资料的原投影、连接和APP选择结果。重复连接不去重。"""
from datetime import timedelta
from django.utils import timezone
from .source_quality_reports import rows, key
from .source_business_updates import matching
from .source_stock_services import raw
from .source_foundation_queries import values
from .source_foundation_scalars import feel_code
from .source_foundation_platform import distinct
from .source_package_labels import varchar

NAMES=['A_GrayID','s_vwCustomer','v_App_Customer','v_APP_EmployeeDevice','v_Customer','v_DyePhase',
       'V_GrayToProduct','V_Stuff','v_KQ_CType','MaxSavePlease','sp_App_GetEmployeePhone',
       'sp_App_O_GetPostList','sp_App_sysGetMFEmpGroup','sp_App_GetAppChildFunctions']


def month_start(value):
    return value.replace(day=1,hour=0,minute=0,second=0,microsecond=0)


def month_end(value):
    return month_start(value.replace(day=28)+timedelta(days=4))-timedelta(milliseconds=3)


def report(name,value='',employee='',query=rows,now=None):
    now=timezone.localtime() if now is None else now
    def source(table):return query(table,'erp_base').order_by('pk')
    output=[]
    if name=='A_GrayID':
        output=[{'GrayID':raw(r,'GrayID'),'NameC':raw(r,'NameC')} for r in source('PGray')]
        output += [{'GrayID':raw(r,'FabricID'),'NameC':raw(r,'CustFabricName')} for r in matching(source('PFabricCust'),Kind='G')]
    elif name in ['s_vwCustomer','v_App_Customer','v_Customer']:
        for customer in source('PCustomer'):
            item=values(customer)
            if name=='s_vwCustomer':
                category=matching(source('PCustCategory'),CustomerID=raw(customer,'CustomerID')).first()
                item['CustCategoryCode']=None if category is None else raw(category,'CustCategoryCode')
            if name=='v_Customer':
                if key(raw(customer,'CustKindID'))!='0' or raw(customer,'RightStatus')!=10:
                    continue
                contacts=list(matching(source('PCustLinker'),CustomerID=raw(customer,'CustomerID')).filter(old_row_no=1))
                output += [{**item,'EbOd':str(int(raw(customer,'EnableOrders') or 0)),
                    'Linker':None if c is None else raw(c,'Name'),'LinkerTel':None if c is None else raw(c,'Mobile')} for c in contacts or [None]]
            else:
                output.append(item)
    elif name=='v_APP_EmployeeDevice':
        output=[values(r) for r in matching(source('HEmployee'),EmpKind='设备部主管') if not raw(r,'IsOut')]
    elif name=='v_DyePhase':
        output=[values(r) for r in matching(source('PFieldValid'),FieldType='DyePhase')]
    elif name=='V_GrayToProduct':
        products=list(source('PProduct'))
        for gray in source('PGray'):
            if raw(gray,'IsStop'):continue
            matches=[p for p in products if raw(p,'ProdID') is not None and key(raw(gray,'GrayID'))==key(raw(p,'ProdID')[1:51])]
            for product in matches or [None]:
                item={f:None if product is None else raw(product,f) for f in ['ProdID','ProdWidth','WidthKindID','ProdWeight','WeightKindID','ProductionID','Spec']}
                item.update(GrayID=raw(gray,'GrayID'),NameC=raw(gray,'NameC'),CustomerID=raw(gray,'NameE'),
                    ProdName=None if product is None else raw(product,'NameC'),FeelCode=feel_code(item['ProdID'],query))
                output.append(item)
    elif name=='V_Stuff':
        for item in source('PStuff'):
            automatic=key(raw(item,'StuffType'))=='S' or key(raw(item,'StuffType'))=='A' and key(raw(item,'AutoSysID'))=='1'
            output.append({**values(item),'AutoID':None if automatic else '0','AutoName':None if automatic else '手工备料',
                'AutoSysIDs':1 if key(raw(item,'AutoSysID'))=='1' else 0})
    elif name=='v_KQ_CType':
        output=[{'sn':raw(r,'Mnemonic'),'Name':raw(r,'Name'),'NumValue':raw(r,'NumValue')}
                for r in matching(source('PFieldValid'),FieldType='CHECKSNTYPE')]
    elif name=='MaxSavePlease':
        for request in source('RequestLimit').filter(old_sheet_date__gt=month_start(now),old_sheet_date__lte=month_end(now)):
            limits=list(matching(source('Limit'),EmpID=raw(request,'DesigneeID')))
            for limit in limits or [None]:
                kind=None if limit is None else raw(limit,'Kind')
                kinds=[] if kind is None else list(source('KindLimit').filter(old_kind=kind))
                for level in kinds or [None]:
                    days=None if level is None else raw(level,'DeliveryDay'); date=raw(request,'SheetDate')
                    deadline=None if days is None else min(date+timedelta(days=days),month_end(date))
                    output.append({'CustomerID':raw(request,'CustomerID'),'SheetDate':date,'SavePleaseDate':deadline,'Kind':kind,'DeliveryDay':days})
    elif name=='sp_App_GetEmployeePhone':
        selected=[] if value is None else [key(v) for v in value.split(';')]
        output=[{'name':raw(r,'Name'),'phone':raw(r,'Mobile')} for r in source('HEmployee')
                if key(raw(r,'EmpID')) in selected or key(raw(r,'Name')) in selected]
    elif name=='sp_App_O_GetPostList':
        output=[{'PostID':raw(r,'Code'),'PostName':raw(r,'Name')} for r in matching(source('PFieldValid'),FieldType='Station')]
        output.sort(key=lambda r:(r['PostID'] is not None,key(r['PostID']) or ''))
    elif name=='sp_App_sysGetMFEmpGroup':
        output=[values(r) for r in matching(source('SDBComboValue'),ComboID='MF_EmpG')]
        output.sort(key=lambda r:(r['DisplayIndex'] is not None,r['DisplayIndex'] or 0))
    elif name=='sp_App_GetAppChildFunctions':
        value,employee=varchar(value,500),varchar(employee,50)
        choices=[r for r in source('SFunctions') if key(value) is not None and key(value) in
                 [key(raw(r,'FuncNo')),key(raw(r,'FuncName')),None if raw(r,'AppURL') is None else key('/pages'+raw(r,'AppURL'))]]
        if choices and raw(choices[0],'RelaFuncNo') is not None:
            current=choices[0];selected=[key(v) for v in varchar(raw(current,'RelaFuncNo'),500).split(';')]
            for role in source('HEmpRole'):
                if key(employee)!='0000' and (employee is None or key(raw(role,'EmpID'))!=key(employee)):continue
                for permission in matching(source('SPermission'),RoleNo=raw(role,'RoleNo')):
                    number=raw(permission,'FuncNo')
                    if number is None or not number.startswith(('90','91')) or key(number) not in selected:continue
                    definitions=list(matching(source('SFunctions'),FuncNo=number))
                    for definition in definitions or [None]:
                        output.append({'text':None if definition is None else raw(definition,'FullName'),
                            'selectedIconPath':None if definition is None else raw(definition,'IconName'),
                            'page':None if definition is None or raw(definition,'AppURL') is None else '/pages'+raw(definition,'AppURL'),
                            'FuncNo':number,'ThisFuncNo':varchar(raw(current,'FuncNo'),10)})
            output=distinct(output)
            if key(value)!='900013':output.append({'text':'首页','selectedIconPath':'t-icon-home','page':'/pages/index/index','FuncNo':'000000','ThisFuncNo':varchar(raw(current,'FuncNo'),10)})
    else:
        raise KeyError(name)
    return {'report':name,'rows':output}
