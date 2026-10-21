"""交付附加项目、合卡号和疵点原函数。逐行连接保留重复及NULL传播。"""
from django.core.exceptions import ValidationError
import re
from .source_quality_reports import rows
from .source_business_updates import matching
from .source_stock_services import raw
from .source_package_labels import varchar
from .source_phase3_operations import model
from .source_trial_steps import equal

NAMES=['fn_CombineSheetNos','fn_ProdOutPriceAtte','GetRecordDefect','get_fsplit_CombineSheetNos']


def calculate(name,p,reader=rows):
    def select(table,**values):
        m=model(table)
        return matching(reader(m.__name__.removeprefix('SourceDye'),m._meta.app_label),**values).order_by('pk')
    evidence=[];value=None
    if name=='get_fsplit_CombineSheetNos':
        text=varchar(p['text'],8000);separator=varchar(p['separator'],10)
        if text is None:return {'report':name,'rows':[]}
        length=None if separator is None else len(separator.rstrip(' '))
        if length==0:raise ValidationError({'separator':'原分隔符为空会使循环无法前进，请填写实际分隔符。'})
        parts=[]
        while text is not None and separator is not None and (found:=re.search(re.escape(separator),text,re.IGNORECASE)) is not None:
            index=found.start();parts.append(text[:index]);text=text[index+length:]
        if text is not None and not equal(text,''):parts.append(text)
        return {'report':name,'rows':[{'JobSheetNo':v} for v in parts]}
    if name=='fn_CombineSheetNos':
        value=''
        for job in select('JobSheet',SheetNo=varchar(p['jobsheetno'],30)):
            for row in select('JobCombine',SheetSeries=raw(job,'SheetSeries')):
                text=raw(row,'JobSheetNo');evidence.append({'job_id':job.pk,'record_id':row.pk,'JobSheetNo':text})
                value=None if text is None else varchar((value or '')+'|'+text,8000)
    elif name=='fn_ProdOutPriceAtte':
        jobs=list(select('JobSheet',SheetNo=varchar(p['jobsheetno'],30)))
        series=None if not jobs else raw(jobs[-1],'SheetSeries')
        for row in select('JobAtte',SheetSeries=series):
            if p['ischarge']==0 and not equal(raw(row,'FieldType'),'05'):continue
            text=raw(row,'AtteValue');description=raw(row,'Description')
            evidence.append({'record_id':row.pk,'AtteValue':text,'Description':description})
            if p['ischarge']!=0 and description is not None and not equal(description,''):
                text=None if text is None else text+':'+description
            value=None if text is None else varchar((value or '')+('-' if p['ischarge']==0 else ',')+text,8000)
    elif name=='GetRecordDefect':
        value=''
        for row in select('RecordDefect',BarCode=varchar(p['barcode'],50)):
            for field in select('p_FieldValid',FieldType='DefectName',Code=raw(row,'DefectID')):
                text=raw(field,'Name');evidence.append({'record_id':row.pk,'dictionary_id':field.pk,'Name':text})
                value=None if value is None or text is None else varchar(value+','+text,8000)
    return {'report':name,'rows':[{'result':value[1:] if value else None}],
        'result_sets':[{'title':'逐行计算来源（不去重）','rows':evidence}],
        'notes':['原字符串拼接没有排序约定，新服务按原行承接顺序计算；候选行全部列出。']}
