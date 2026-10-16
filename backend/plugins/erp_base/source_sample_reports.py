"""打样对色责任、原计件产量、7:30工作日及明确的逐日展开。"""
from plugins.erp_base.source_provenance import reference as source_reference
from collections import defaultdict
from datetime import datetime,timedelta
from decimal import Decimal,ROUND_HALF_UP,localcontext
import re
from django.utils import timezone
from .source_stock_services import raw
from .source_quality_reports import rows,key,total
from .source_business_updates import matching

COUNTERS=['DNum','WNum','TNum','MNum','FWNum','FTNum','FDNum']


def rounded(value,scale='.01'):
    return None if value is None else Decimal(str(value)).quantize(Decimal(scale),rounding=ROUND_HALF_UP)


def float_round(value):
    with localcontext() as context:
        context.prec=340  # SQL float(53)有限数的十进制整数部分及两位小数。
        return float(Decimal.from_float(float(value)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))


def recipe_dictionary(query,issues):
    result=[]
    for item in matching(query('PFieldValid','erp_base'),FieldType='RecipeKind').order_by('pk'):
        code=raw(item,'Code')
        if code is None:continue
        stripped=code.strip()
        if stripped and (re.fullmatch(r'[+-]?[0-9]+',stripped) is None or not -2147483648<=int(stripped)<=2147483647):
            issues.append({'record_id':item.pk,'source': source_reference(item),'Code':code,'issue':'原整数连接会转换失败；此字典原行保留，本次无法关联计件'})
        else:result.append((0 if stripped=='' else int(stripped),item))
    return result


def source_rows(start,end,query=rows):
    result=[];excluded=[]
    for table in ['DyeDipsRecord','DyeReprint']:
        source=query(table,'erp_sampling')
        if start is not None:source=source.filter(old_sheet_date__gte=start)
        if end is not None:source=source.filter(old_sheet_date__lt=end)
        for item in source.order_by('pk'):
            emp=raw(item,'EmpID');version=raw(item,'ColorVersion') if table=='DyeDipsRecord' else ''
            if key(emp or '')=='' or table=='DyeDipsRecord' and key('A' if version is None else version)!='A':
                excluded.append({'entity':item._meta.label,'record_id':item.pk,'source': source_reference(item),'issue':'原主工号为空或普通打样版本不是A'});continue
            stamp=raw(item,'SheetDate');kind=raw(item,'IsDoubleDye' if table=='DyeDipsRecord' else 'Kind')
            row={name:raw(item,name) for name in ['SheetDate','EmpID','ColorNum','ColorID','CustomerID','SheetNo']}
            row.update(entity=item._meta.label,record_id=item.pk,source=source_reference(item),ID=f'{table}:{item.pk}',
                SheetKind=4 if table=='DyeDipsRecord' else raw(item,'SheetKind'),ColorVersion=version,
                JobSheetNo='' if table=='DyeDipsRecord' else raw(item,'JobSheetNo'),IsDoubleDye=kind,
                SDate=None if stamp is None else (timezone.localtime(stamp)-timedelta(minutes=450)).date().isoformat(),
                Num=float_round(1 if raw(item,'Num') is None else raw(item,'Num')))
            row.update({name:0 for name in COUNTERS})
            if table=='DyeDipsRecord':
                row['DNum']=int((kind or 0)==0);row['WNum']=int(kind==1)
            elif kind in range(1,7):row[COUNTERS[kind]]=1
            result.append(row)
    return result,excluded


def checker(start,end,query=rows):
    cutoff=timezone.make_aware(datetime(2021,4,18));groups={};details=[]
    for item in query('DyeDipsRecord','erp_sampling').filter(old_sheet_date__gte=max(start,cutoff),old_sheet_date__lte=end).order_by('pk'):
        times=raw(item,'Times')
        for name,field,eligible in [('S','EmpID',True),('R','CheckerID',times is not None and times>1)]:
            employee=raw(item,field)
            if not eligible or key(employee or '')=='':continue
            group=groups.setdefault(key(employee),{'CheckerID':employee,'S':0,'R':0});group[name]+=1
            details.append({'record_id':item.pk,'source': source_reference(item),'measure':name,'employee':employee,'SheetDate':raw(item,'SheetDate')})
    result=[]
    for group in groups.values():
        group['Rate']=Decimal(0) if group['S']==0 else rounded(group['R']/group['S'],'.001')*100
        result.append({'StartDate':start,'EndDate':end,**group})
    return {'report':'Sp_DyeDipsRecord_CheckerID1','rows':result,'result_rows':details,
        'notes':['起点2021-04-18；开始和结束时间都包含。S按EmpID，R按Times>1的CheckerID，不擅自改成同一员工字段。',
            '比值先保留三位小数再乘100；只有R没有S时Rate按原式为0。']}


def production(mode,start=None,end=None,employee=None,query=rows):
    source,excluded=source_rows(start,end,query)
    if employee is not None:source=[row for row in source if key(row['EmpID'])==key(employee)]
    if mode=='details':result=source
    elif mode=='days':
        groups={}
        for row in source:
            group=groups.setdefault(key(row['EmpID']),{'EmpID':row['EmpID'],'days':set()});group['days'].add(row['SDate'])
        result=[{'EmpID':group['EmpID'],'WorkDays':len(group['days'])} for group in groups.values()]
        if employee is not None and not result:result=[{'EmpID':employee,'WorkDays':None}]
    else:
        dictionary=recipe_dictionary(query,excluded)
        groups={}
        for row in source:
            matches=[item for number,item in dictionary if row['IsDoubleDye'] is not None and number==row['IsDoubleDye']]
            if not matches:excluded.append({**row,'issue':'原RecipeKind内连接无匹配，明细仍保留'})
            for item in matches:
                groupkey=(key(row['EmpID']),row['SDate'] if mode=='daily' else None)
                group=groups.setdefault(groupkey,{'EmpID':row['EmpID'],'SDate':groupkey[1],'SumNum':[],**{name:[] for name in COUNTERS},'Amount':[]})
                group['SumNum'].append(row['Num'])
                for name in COUNTERS:group[name].append(row[name])
                factor=sum(row[name] for name in COUNTERS if name!='FDNum')
                price=raw(item,'NumValue');group['Amount'].append(None if price is None else factor*price)
        result=[{**{name:group[name] for name in ['EmpID','SDate']},'SumNum':float_round(total(group['SumNum'])),
            **{name:rounded(total(group[name])) for name in [*COUNTERS,'Amount']}} for group in groups.values()]
    return {'report':{'summary':'qryDyeDipsRecord','daily':'打样工作日报（原产量按SDate展开）','days':'fn_GetDay_DyeDipsRecord_EmpID','details':'vw_DyeDipsRecord_EmpID'}[mode],
        'rows':result,'result_rows':source if mode!='details' else [],'supplemental_rows':excluded,
        'notes':['时间范围为原SheetDate开始包含、结束不含；SDate按本地时间减450分钟。日报是明确的SDate展开，不虚称存在同名原日报过程。',
            '原主EmpID列有效，其他员工UNION已注释；计件按字典连接倍数，Amount不乘Num且排除FDNum，未按常识改算。',
            '视图原NEWID每次随机，页面用来源表/项目ID稳定追溯，不作为原键及来源信息。非数字RecipeKind原整数转换失败需另列异常。']}


def emp1(start=None,end=None,employee=None,query=rows):
    issues=[];dictionary=recipe_dictionary(query,issues);groups={};details=[]
    for table in ['DyeDipsRecord','DyeReprint']:
        source=query(table,'erp_sampling')
        if start is not None:source=source.filter(old_sheet_date__gte=start)
        if end is not None:source=source.filter(old_sheet_date__lt=end)
        for item in source.order_by('pk'):
            emp=raw(item,'EmpID1');kind=raw(item,'SheetKind')
            if employee is not None and key(emp)!=key(employee):continue
            matches=[row for number,row in dictionary if kind is not None and kind==number]
            if not matches:issues.append({'record_id':item.pk,'entity':item._meta.label,'issue':'原SheetKind到RecipeKind无匹配'})
            for dictionary_row in matches:
                group=groups.setdefault(key(emp),{'EmpID1':emp,'DaBan':0,'FuBan':0,'Amount':[]})
                field='DaBan' if table=='DyeDipsRecord' else 'FuBan';group[field]+=1;group['Amount'].append(raw(dictionary_row,'NumValue'))
                details.append({'record_id':item.pk,'entity':item._meta.label,'dictionary_id':dictionary_row.pk,'EmpID1':emp,'measure':field})
    return {'report':'PryDyeProofing','rows':[{**group,'Amount':total(group['Amount'])} for group in groups.values()],
        'result_rows':details,'supplemental_rows':issues,'notes':['独立保留原EmpID1和SheetKind口径，包括空工号分组；不与主EmpID/IsDoubleDye产量混用。',
            '时间筛选为本次明确查询范围；原界面1=2为空数据集占位，不作为永久停用依据。仅核对计件业务，不建立工资支付或财务流程。']}
