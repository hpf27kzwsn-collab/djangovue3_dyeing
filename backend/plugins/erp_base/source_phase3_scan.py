"""坯料/半成品扫码领用查询；保留全部扫码匹配，不合并来源记录。"""
from .source_phase3_operations import SPECS,query
from .source_business_updates import matching
from .source_stock_services import raw
from .source_trial_steps import equal
from .source_quality_reports import rows


def report(code,barcode,job,reader=rows):
    spec=SPECS[code];temps=dict(spec['temps']);p={'barcode':barcode,'jobsheetno':job}
    if code=='373':
        jobs=list(matching(reader('JobSheet','erp_production'),SheetNo=job).order_by('pk')[:1])
        jobbarcode=None if not jobs else raw(jobs[0],'BarCode')
        if equal(barcode or '',job or '') or equal(barcode or '',jobbarcode or ''):
            temps['semistock']='('+temps['semistock']+') UNION ALL ('+spec['inserts'][0]['sql']+')'
    stock=query('SELECT * FROM #'+('graystock' if code=='301' else 'semistock'),p,temps,reader)
    assigned=query('SELECT * FROM #ja',p,temps,reader)
    available=query('SELECT * FROM #'+('g_stock' if code=='301' else 's_stock'),p,temps,reader)
    matched=stock[:1];first=assigned[:1];status=0;message=''
    if not stock:status=1;message="没查询到条码'"+barcode+"'数据！"
    else:
        fields=['grayid','lotno'] if code=='301' else ['lotno','prodid']
        for field in fields:
            old=None if not first else first[0][field]
            if not equal(old or '',matched[0][field] or ''):
                status=1;message="条码'"+barcode+"'的"+('批号' if field=='lotno' else '规格')+'与流程卡不一致，请检查！';break
    output=[]
    for a in assigned or [{}]:
        for b in available or [{}]:
            output.append({'code':status,'msg':message,'customerid':a.get('semi_owner'),**a,'inputcode':b.get('inputcode'),
                **{f:None if equal(barcode,job) else b.get(f) for f in ['packs','rolls','weightqty']},
                **{'kc'+f:b.get(f) for f in ['packs','rolls','weightqty']}})
    return {'report':'Sp_GrayStockToJobOut' if code=='301' else 'Sp_SemiStockToJobOut','rows':output,
        'result_sets':[{'title':'原条码匹配行','rows':stock}]}
