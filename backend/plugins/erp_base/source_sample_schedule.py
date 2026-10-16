"""客样颜色到普通/复版打样排单，按原主从投影承接。"""
from plugins.erp_base.source_provenance import reference as source_reference
from django.db import transaction
from .business import snapshot
from .source_stock_services import raw
from .source_business_updates import matching
from .source_package_operations import reader, scoped, check_scope
from .source_sample_flow import COLOR_FIELDS
from .source_continuation import save_effect


def preview(color,query=reader):
    labs=list(matching(reader('DyeLabMain','erp_sampling'),SheetSeries=raw(color,'SheetSeries')).order_by('pk'))
    existing=list(matching(reader('DyeDipsRecord','erp_sampling'),ColorNum=raw(color,'ColorNum')).order_by('pk'))
    check_scope([color,*labs,*existing],query)
    # 原ColorNum NOT IN (SELECT ISNULL(ColorNum,''))保留NULL排除及空色号对应。
    number=raw(color,'ColorNum')
    empty_exists=reader('DyeDipsRecord','erp_sampling').filter(old_color_num__isnull=True).exists() if number is not None and number.rstrip(' ')=='' else False
    return {'report':'客样打样排单来源','rows':[{'record_id':color.pk,'source': source_reference(color),'ColorNo':raw(color,'ColorNo'),
        'ColorNum':number,'original_visible':number is not None and not existing and not empty_exists}],
        'candidate_rows':[{'record_id':row.pk,'source': source_reference(row),'CustomerID':raw(row,'CustomerID'),'selected':row.pk==labs[-1].pk} for row in labs],
        'supplemental_rows':[{'record_id':row.pk,'SheetSeries':raw(row,'SheetSeries'),'issue':'已有同色号打样；原未打样选择器不再显示，仍可明确复版'} for row in existing],
        'notes':['原来样表头LEFT JOIN及全部颜色字段保留；缺失表头不补造。多表头按项目ID最后候选采用并留存候选。',
            '普通打样和复版沿用原入口号码、部门及最新字段；已有打样不阻止明确复版。']},labs


@transaction.atomic
def schedule(color,actor,entry,version,employee,shift,at,reason,query=reader):
    from .source_services import write
    color=scoped(color,query);report,labs=preview(color,query)
    model=reader('DyeDipsRecord','erp_sampling').model
    fields={name:raw(color,name) for name in COLOR_FIELDS if name in model.SOURCE_FIELDS}
    if labs:
        parent=labs[-1]
        fields.update({name:raw(parent,name) for name in ['BusinessUnitID','CustomerID','SalerGroupID','SalerID','VerLight1ID','VerLight2ID']})
    fields.update(SheetDate=at,ColorVersion=version,EmpID=employee,ShiftID=shift)
    values={model.SOURCE_FIELDS[name]:value for name,value in fields.items()}
    target=write(model,{'_entry':entry,**values},actor=actor,apply_effects=False)
    save_effect(target,'sample_schedule_origin',{'source':snapshot(color),'source_entity':color._meta.label,
        'headers':[snapshot(row) for row in labs],'at':at,'reason':reason,'report':report},actor,reason)
    return target
