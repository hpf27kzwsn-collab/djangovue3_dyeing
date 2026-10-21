"""原XML报表汇总及计算字段依赖；原声明保留，只执行实际被引用的字段。"""
import re
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError


def formatting_usage(root):
    """规则库与实际引用分开；未引用定义原样保留，不当成已执行规则。"""
    sheet=root.find('FormattingRuleSheet')
    definitions=[] if sheet is None else list(sheet)
    stored={id(n) for n in sheet.iter()} if sheet is not None else set()
    references={v for n in root.iter() if id(n) not in stored for v in n.attrib.values() if v.startswith('#Ref-')}
    active=[n.get('Name') for n in definitions if '#Ref-'+n.get('Ref','') in references]
    collections=[n for n in root.iter() if n.tag=='FormattingRules' and (len(n) or n.attrib)]
    return {'active':active,'unreferenced':[n.get('Name') for n in definitions if '#Ref-'+n.get('Ref','') not in references],
        'has_assignments':bool(active or collections or any(n.get('FormattingRules') for n in root.iter()))}


def calculation_usage(root):
    from .source_phase6_calculated_print import reference_names
    definitions={node.get('Name'):node for node in root.findall('./CalculatedFields/*')}
    actual={name.lower():name for name in definitions}
    references={node.get('DataMember','').split('.')[-1] for node in root.findall('.//DataBindings/*')}
    references.update(node.get('FieldName') for group in ['GroupFields','SortFields'] for node in root.findall('.//'+group+'/*') if node.get('FieldName'))
    references.update(re.findall(r'\[([^]]+)\]',root.get('FilterString','')))
    active={actual[name.lower()] for name in references if name.lower() in actual}
    pending=list(active)
    while pending:
        name=pending.pop()
        children={actual[ref.lower()] for ref in reference_names(definitions[name].get('Expression',''))
                  if ref.lower() in actual}-active
        active.update(children);pending.extend(children)
    return {'active':sorted(active),'unreferenced':sorted(set(definitions)-active)}


def summary_issues(node):
    issues=[]
    if node.get('Running','None')=='None':return issues
    if node.get('Running','None') not in ['Report','Group','Page']:issues.append('未实现汇总范围：'+node.get('Running','None'))
    if node.get('Func','Sum') not in ['Sum','Count','Avg','Min','Max','RecordNumber']:issues.append('未实现汇总函数：'+node.get('Func'))
    return issues


def summarize(values, rule):
    operation=rule.get('Func','Sum')
    included=[v for v in values if v is not None] if rule.get('IgnoreNullValues','false')=='true' else [0 if v is None else v for v in values]
    if operation=='Count':return len(included)
    if rule.get('TreatStringsAsNumerics','true')=='true':
        try:
            included=[Decimal(v) if isinstance(v,str) else v for v in included]
        except InvalidOperation as error:
            raise ValidationError({'summary':'此原数值汇总存在不能转换为数值的原行；不能跳过该行或作为0打印。'}) from error
    elif operation in ['Min','Max'] and included and all(isinstance(v,str) for v in included):
        # 明确采用 Unicode 排序；旧客户端区域排序仍待原运行结果核对。
        return (min if operation=='Min' else max)(included)
    if any(not isinstance(v,(int,float,Decimal)) for v in included):
        raise ValidationError({'summary':'此原数值汇总存在非数值原行；原值保留，不能作为0继续打印。'})
    included=[Decimal(str(v)) for v in included]
    if operation=='Sum':return sum(included,Decimal(0))
    if not included:return None
    if operation=='Avg':return sum(included,Decimal(0))/len(included)
    return (min if operation=='Min' else max)(included)
