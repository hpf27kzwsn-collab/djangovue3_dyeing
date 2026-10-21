"""原XML固定高度版式的填数校样。复杂脚本/分组逐项报告，不输出缺数据的假成品。"""
import base64
import re
from string import Formatter
from datetime import date, datetime
from decimal import Decimal
from html import escape
from django.core.exceptions import ValidationError
from django.utils import timezone
from .source_phase6_layouts import describe, parse_xml, kind
from .source_phase6_print_rules import calculation_usage, summary_issues, summarize, formatting_usage
from . import source_phase6_calculated_print as calculations
from . import source_phase6_qr_print as qr_print
from . import source_phase6_text_scripts as text_scripts
from .source_phase6_print_sources import binding_field,source_issue,projections,PROJECTION_NOTES
from .source_phase6_print_groups import arrange,level

BANDS = {'DetailBand', 'TopMarginBand', 'BottomMarginBand', 'ReportHeaderBand',
         'ReportFooterBand', 'PageHeaderBand', 'PageFooterBand', 'GroupHeaderBand','GroupFooterBand'}
CONTROLS = {'XRTable', 'XRTableRow', 'XRTableCell', 'XRLabel', 'XRLine', 'XRPageInfo', 'XRBarCode'}


def projection_names(tree):
    """按现存原表展开SELECT *，避免缺列的模板被星号误判为可填数。"""
    from django.apps import apps
    from sqlglot import exp
    from sqlglot.optimizer.scope import build_scope,Scope
    fields={m.SOURCE_TABLE.lower():{n.lower() for n in m.SOURCE_FIELDS}
        for m in apps.get_models() if hasattr(m,'SOURCE_FIELDS')}
    def source_names(source):
        if isinstance(source,Scope):return names(source)
        return fields.get(source.name.lower(),{'*'})
    def names(scope):
        if isinstance(scope.expression,exp.Union):return names(scope.set_operation_scopes[0])
        result=set()
        for node in scope.expression.expressions:
            if node.is_star:
                sources=[scope.sources[node.table]] if isinstance(node,exp.Column) and node.table else scope.sources.values()
                for source in sources:result.update(source_names(source))
            else:result.add(node.alias_or_name.lower())
        return result
    return names(build_scope(tree))


def reference_columns(row, result, reader):
    """原客户端_R显示列：资料名按原选择器取数，缺枚举定义明确打印原代码。"""
    entry = result['entry']
    root, _ = parse_xml(base64.b64decode(row['TemplateXml']))
    calculation_plan=calculations.plan(root)
    calculated_names={node.get('Name').lower() for node,_ in calculation_plan}
    calculated_inputs={ref for _,tree in calculation_plan for ref in calculations.references(tree) if ref.lower() not in calculated_names}
    requested = sorted(calculated_inputs | set(text_scripts.inputs(root)) | {b.get('DataMember')[len(entry)+1:] for b in root.findall('.//DataBindings/*')
                        if b.get('DataMember', '').startswith(entry+'.')} |
                       {f.get('FieldName') for f in [*root.findall('.//GroupFields/*'),*root.findall('.//SortFields/*')]})
    return resolve_reference_columns(result,requested,reader)


def reference_available(entry,name,projected):
    from .source_phase6_entries import definition
    fields={f['FieldName'].lower():f for f in definition(entry)['fields']}
    return name.lower().endswith('_r') and name[:-2].lower() in projected and name[:-2].lower() in fields and fields[name[:-2].lower()]['EditorKind'] in ['Lookup','Lookup_NoCheck','DBCombo','DBCombo_Edit','Enum','MulitCheck']


def resolve_reference_columns(result,requested,reader):
    """同一原入口的显示字段；供本行与明确父单共同使用，保留重复候选。"""
    from .source_phase6_entries import definition
    from .source_foundation_queries import lookup,combo
    from .source_trial_steps import equal
    fields={f['FieldName'].lower():f for f in definition(result['entry'])['fields']}
    result = {**result, 'columns': list(result['columns']), 'rows': [list(values) for values in result['rows']]}
    names = [c['name'].lower() for c in result['columns']];resolutions = list(result.get('reference_resolutions',[]))
    for name in requested:
        if name.lower() in names or not name.lower().endswith('_r'):continue
        base = name[:-2];rule = fields[base.lower()]
        if names.count(base.lower()) != 1:
            raise ValidationError({'binding': '原显示列的代码来源不是唯一投影：'+base})
        pos = names.index(base.lower());kind = rule['EditorKind'];code = rule['EditorID']
        if kind in ['Lookup','Lookup_NoCheck']:
            data = lookup(code,query=reader)
            if not data['implemented']:raise ValidationError({'binding':data})
            candidates = data['rows']
        elif kind in ['DBCombo','DBCombo_Edit']:candidates = combo(code,'',query=reader)['rows']
        elif kind in ['Enum','MulitCheck']:candidates = []
        else:raise ValidationError({'binding': '原显示列尚无取数对应：'+name+'/'+str(kind)})
        result['columns'].append({'name':name});names.append(name.lower())
        for index, values in enumerate(result['rows']):
            original = values[pos]
            matches = [option for option in candidates if equal(str(option['id']) if option['id'] is not None else None,
                                                               str(original) if original is not None else None)]
            labels = [option['text'] for option in matches]
            if kind in ['Enum','MulitCheck']:
                text = None if original is None else '原代码：'+str(original)
                state = '多选串分隔约定未证明，完整原代码校样' if kind=='MulitCheck' else '缺客户端枚举定义，按原代码校样'
            elif not labels:
                text = None if original is None else '未对应代码：'+str(original)
                state = '无资料匹配，原代码保留'
            elif len(set(labels)) == 1:text = labels[0];state = '原资料显示名'
            else:
                text = '候选：'+' / '.join('〈NULL〉' if label is None else str(label) for label in labels)
                state = '重复代码有不同名称，全部列出'
            values.append(text)
            resolutions.append({'row':index,'field':name,'source_code':original,'state':state,'candidates':matches})
    result['reference_resolutions'] = resolutions
    return result


def requirements(row):
    if row['TemplateXml'] is None:
        return ['缺原XML版式']
    root, _ = parse_xml(base64.b64decode(row['TemplateXml']))
    issues = []
    if root.get('DataMember')=='GrayStockInAndOut':
        issues.append('原库存数量是客户端待填的0占位；缺期间结存和退料分类填数来源，不能作为真实库存打印')
    if formatting_usage(root)['has_assignments']:
        issues.append('未实现原格式规则引用：FormattingRules')
    if not root.get('DataMember'):
        issues.append('原模板未声明数据入口')
    layout=describe(row)
    margins=[float(v) for v in layout['page'].get('Margins','0,0,0,0').split(',')]
    minimum=sum(b['height'] for b in layout['bands'] if b['kind'] in ['DetailBand','PageHeaderBand','PageFooterBand'])
    if minimum>float(layout['page']['PageHeight'])-margins[2]-margins[3]+1e-6:
        issues.append('原固定明细及页眉页脚高度超过纸张可用高度；原裁切/缩放设置未核对')
    groups = [node for node in root.iter() if kind(node) == 'GroupHeaderBand']
    footers = [node for node in root.iter() if kind(node) == 'GroupFooterBand']
    levels=[int(g.get('Level','0')) for g in groups]
    footer_levels=[int(g.get('Level','0')) for g in footers]
    if len(set(levels))!=len(levels) or len(set(footer_levels))!=len(footer_levels):issues.append('原分组Level重复，组头/组尾无法唯一对应')
    if groups and any(v not in levels for v in footer_levels):issues.append('组尾缺同Level的组头')
    for footer in footers:
        if footer.get('GroupUnion','None') not in ['None','WithLastDetail']:
            issues.append('未实现此组尾整体规则')
    for group in groups:
        fields = list(group.findall('./GroupFields/*'))
        if any(not f.get('FieldName') or f.get('SortOrder','Ascending') not in ['Ascending','Descending'] for f in fields):
            issues.append('未实现原分组字段或排序规则')
        if group.get('PageBreak','None') not in ['BeforeBand','None']:
            issues.append('未实现此分组分页方式')
        if group.get('GroupUnion','None') not in ['None','WholePage','WithFirstDetail']:
            issues.append('未实现此分组整体规则')
    for node in root.iter():
        control = kind(node)
        if control=='XRBarCode':issues.extend(qr_print.issues(node,root))
        if control == 'XRPageInfo':
            if node.get('PageInfo','NumberOfTotal') not in ['Number','NumberOfTotal','DateTime','None']:
                issues.append('未实现页码类型：'+node.get('PageInfo'))
            if node.get('RunningBand') or node.get('StartPageNumber','1') != '1':
                issues.append('未实现分组页码或自定义起始页码')
        if node.find('Summary') is not None and node.find('Summary').get('Running','None')!='None' and len(node.findall('./DataBindings/*[@PropertyName="Text"]')) != 1 and node.find('Summary').get('Func')!='RecordNumber':
            issues.append('汇总未唯一绑定Text来源：'+str(node.get('Name')))
        if control and control not in BANDS | CONTROLS | {'XRMainReport', 'XtraReport'}:
            issues.append('未实现控件/分组：'+control)
        if node.tag == 'CalculatedFields' and calculation_usage(root)['active']:
            issues.extend(calculations.issues(root))
        if node.tag == 'Summary':
            issues.extend(summary_issues(node))
            if node.get('Running')=='Group' and not groups and not footers:issues.append('组汇总缺分组')
        if node.tag == 'SortFields':
            if any(not f.get('FieldName') or f.get('SortOrder','Ascending') not in ['Ascending','Descending'] for f in node):
                issues.append('未实现明细排序规则')
            if not any(node is b.find('SortFields') for b in root.iter() if kind(b)=='DetailBand'):
                issues.append('未实现此位置的SortFields')
        inactive_columns=node.tag=='MultiColumn' and (node.get('Mode','None')=='None' or node.get('Mode')=='UseColumnCount' and int(node.get('ColumnCount','1'))==1)
        if node.tag in ['Scripts', 'ExpressionBindings', 'MultiColumn'] and (len(node) or node.attrib) and not inactive_columns and not (node.tag=='Scripts' and (qr_print.script_event(node,root) or text_scripts.script_event(node,root))):
            issues.append('未实现原规则：'+node.tag)
        for name in ['ScriptsSource', 'ScriptSource', 'FilterString', 'StyleName', 'OddStyleName', 'EvenStyleName']:
            if node.get(name) and not (name=='ScriptsSource' and node is root and (qr_print.supported_script(root) or text_scripts.plan(root) is not None)):
                issues.append('未实现原属性：'+name)
        for name in ['Angle', 'TextAngle']:
            if float(node.get(name, '0')) != 0:
                issues.append('未实现文字旋转：'+name)
        for name in ['CanGrow', 'CanShrink']:
            if node.get(name) == 'true':
                issues.append('未实现动态高度：'+name)
        if node.get('PageBreak', 'None') != 'None' and not (control == 'GroupHeaderBand' and node.get('PageBreak') == 'BeforeBand'):
            issues.append('未实现显式分页：'+node.get('PageBreak'))
        if node.tag == 'DataBindings':
            for binding in node:
                if binding.get('PropertyName') not in ['Text','Bookmark','Tag']:
                    issues.append('未实现属性绑定：'+str(binding.get('PropertyName')))
                if not binding.get('DataMember', '').startswith(root.get('DataMember', '')+'.'):
                    issue=source_issue(root.get('DataMember'),binding.get('DataMember','')) if root.get('DataMember') else '缺跨表关联：'+binding.get('DataMember','')
                    if issue:issues.append(issue)
    if not issues:
        # 对显式列查询核对原版式绑定；能排出几何不代表当前查询仍提供旧列。
        from .source_phase6_entries import tree_for, definition
        entry=root.get('DataMember')
        projected=projection_names(tree_for(entry))
        from sqlglot import parse_one
        projected.update(parse_one(value,read='tsql').alias_or_name.lower() for value in projections(entry))
        computed={node.get('Name').lower() for node,_ in calculations.plan(root)}
        required_inputs={ref for _,tree in calculations.plan(root) for ref in calculations.references(tree)} | set(text_scripts.inputs(root))
        if '*' not in projected:
            fields={f['FieldName'].lower():f for f in definition(entry)['fields']}
            for binding in root.findall('.//DataBindings/*'):
                if not binding.get('DataMember').startswith(entry+'.'):continue
                name=binding.get('DataMember')[len(entry)+1:].lower()
                display=(name.endswith('_r') and name[:-2] in projected and name[:-2] in fields
                         and fields[name[:-2]]['EditorKind'] in ['Lookup','Lookup_NoCheck','DBCombo','DBCombo_Edit','Enum','MulitCheck'])
                if name not in projected and name not in computed and not display:
                    issues.append('当前原查询未提供版式字段：'+binding.get('DataMember'))
            for field in [*root.findall('.//SortFields/*'),*root.findall('.//GroupFields/*')]:
                name=field.get('FieldName').lower()
                display=(name.endswith('_r') and name[:-2] in projected and name[:-2] in fields
                         and fields[name[:-2]]['EditorKind'] in ['Lookup','Lookup_NoCheck','DBCombo','DBCombo_Edit','Enum','MulitCheck'])
                if name not in projected and name not in computed and not display:
                    issues.append('当前原查询未提供排序/分组字段：'+field.get('FieldName'))
            for ref in required_inputs:
                name=ref.lower()
                display=(name.endswith('_r') and name[:-2] in projected and name[:-2] in fields
                    and fields[name[:-2]]['EditorKind'] in ['Lookup','Lookup_NoCheck','DBCombo','DBCombo_Edit','Enum','MulitCheck'])
                if name not in projected and name not in computed and not display:
                    issues.append('当前原查询未提供计算来源：'+ref)
    return list(dict.fromkeys(issues))


def formatted(value, pattern=''):
    if value is None:
        return ''
    if not pattern:
        return str(value)
    match = re.fullmatch(r'\{0:([^}]+)\}', pattern)
    if match is None:
        parts=[]
        for literal,field,spec,conversion in Formatter().parse(pattern):
            parts.append(literal)
            if field is not None:
                if field!='0' or conversion:raise ValidationError({'format':'未对应原复合格式：'+pattern})
                parts.append(formatted(value,'{0:'+spec+'}' if spec else ''))
        return ''.join(parts)
    spec = match[1]
    # .NET String不是IFormattable；原地址误带日期格式时仍输出字符串原文。
    if isinstance(value,str):return value
    if isinstance(value, (date, datetime)):
        if isinstance(value, datetime) and timezone.is_aware(value):
            value = timezone.localtime(value)
        from .source_phase6_date_format import format_date
        return format_date(value,spec)
    if re.fullmatch(r'[nNfF]\d*', spec):
        places = int(spec[1:] or '2')
        return format(Decimal(value), (',' if spec[0].lower() == 'n' else '')+'.'+str(places)+'f')
    if re.fullmatch(r'[#0,]+(?:\.[#0]+)?', spec):
        fraction = spec.split('.')[1] if '.' in spec else ''
        text = format(Decimal(value), (',' if ',' in spec else '')+'.'+str(len(fraction))+'f')
        if '0' not in spec and Decimal(text.replace(',','')) == 0:return ''
        for _ in range(len(fraction)-len(fraction.rstrip('#'))):
            if text.endswith('0'):text = text[:-1]
        return text.rstrip('.')
    raise ValidationError({'format': '尚未实现的原格式：'+pattern})


def color(value):
    if not value:return None
    if value == 'Transparent':return 'transparent'
    if re.fullmatch(r'[A-Za-z]+', value):return value
    parts = [int(v.strip()) for v in value.split(',')]
    if len(parts) == 4:
        a, r, g, b = parts
        return f'rgba({r},{g},{b},{a/255})'
    return 'rgb('+','.join(str(v) for v in parts)+')'


def render(row, result):
    problems = requirements(row)
    if problems:
        raise ValidationError({'layout': problems})
    layout = describe(row)
    entry = layout['data_member']
    if result['entry'] != entry:
        raise ValidationError({'entry': '原版式声明的数据入口与查询不一致。'})
    root,_=parse_xml(base64.b64decode(row['TemplateXml']))
    generated_at=timezone.localtime(timezone.now())
    result=calculations.apply(root,result,generated_at)
    columns = {}
    for index, column in enumerate(result['columns']):
        columns.setdefault(column['name'].lower(), []).append(index)
    dpi = float(layout['page'].get('Dpi', '100'))
    mm = 25.4/dpi
    width = float(layout['page']['PageWidth']);height = float(layout['page']['PageHeight'])
    left, right, top, bottom = [float(v) for v in layout['page'].get('Margins', '0,0,0,0').split(',')]
    bands = {name: [b for b in layout['bands'] if b['kind'] == name] for name in BANDS}
    rows = list(result['rows'])
    root, _ = parse_xml(base64.b64decode(row['TemplateXml']))
    sort_fields=[field for band in root.iter() if kind(band)=='DetailBand' for field in band.findall('./SortFields/*')]
    for field in reversed(sort_fields):
        candidates=columns.get(field.get('FieldName').lower(),[])
        if len(candidates)!=1:raise ValidationError({'sort':'排序字段无法唯一定位：'+field.get('FieldName')})
        position=candidates[0]
        rows.sort(key=lambda values:(values[position] is not None,values[position]),
                  reverse=field.get('SortOrder','Ascending')=='Descending')
    from .source_phase6_print_groups import report_headers
    headers,group_rows,group_starts,group_ends=arrange(rows,report_headers(bands['GroupHeaderBand'],bands['GroupFooterBand']),root,columns)
    detail_height = sum(b['height'] for b in bands['DetailBand'])
    footer_height = sum(b['height'] for b in bands['PageFooterBand'])
    if detail_height <= 0 and not headers:
        raise ValidationError({'layout': '原明细没有可分页高度。'})

    metadata_bindings=[]
    bookmarks=[]
    script_plan=text_scripts.active_plan(root)
    def control_html(control, values, scope, page_rows, page_number, page_count):
        if control['attributes'].get('Visible') == 'false':return ''
        text = control['text']
        if control['kind']=='XRPageInfo':
            from .source_phase6_page_info import page_info
            text=page_info(control['attributes'],page_number,page_count,generated_at)
        if control['summary'] and control['summary'].get('Func')=='RecordNumber' and control['summary'].get('Running','None')!='None':
            rule=control['summary']
            number_rows=scope if rule.get('Running')=='Group' else page_rows if rule.get('Running')=='Page' else rows
            text=formatted(next((i for i,row in enumerate(number_rows or [],1) if row is values),0),rule.get('FormatString',''))
        attributes={}
        for binding in control['bindings']:
            field = binding_field(entry,binding['DataMember'])
            candidates = columns.get(field.lower(), [])
            if len(candidates) != 1:
                raise ValidationError({'binding': binding['DataMember']+'无法唯一定位，投影位置：'+str(candidates)})
            if binding['PropertyName'] in ['Bookmark','Tag']:
                value=values[candidates[0]];label=formatted(value,binding.get('FormatString',''))
                metadata_bindings.append({'control':control['name'],'page':page_number,'property':binding['PropertyName'],
                    'source':binding['DataMember'],'value':value,'formatted':label})
                if binding['PropertyName']=='Tag':attributes['data-legacy-tag']=label
                else:
                    anchor='original-bookmark-'+str(len(bookmarks)+1)
                    attributes['id']=anchor
                    bookmarks.append({'anchor':anchor,'text':label,'page':page_number,'is_null':value is None})
                continue
            if control['summary'] and control['summary'].get('Running','None')!='None':
                rule=control['summary']
                if rule.get('Running')=='Group' and scope is None:
                    text='?'
                else:
                    summary_rows=scope if rule.get('Running')=='Group' else page_rows if rule.get('Running')=='Page' else rows
                    # 行序号以原行位置计，不能用值相等定位，否则重复行会打印相同序号。
                    value=next((i for i,row in enumerate(summary_rows,1) if row is values),0) if rule.get('Func')=='RecordNumber' else summarize([r[candidates[0]] for r in summary_rows],rule)
                    text=formatted(value,rule.get('FormatString',binding.get('FormatString','')))
            else:
                text = formatted(values[candidates[0]], binding.get('FormatString', ''))
        if script_plan is not None and control['name']==script_plan[1]:
            def script_value(name):
                positions=columns.get(name.lower(),[])
                if len(positions)!=1:raise ValidationError({'script_source':'原文字事件字段无法唯一定位：'+name})
                return values[positions[0]]
            text=text_scripts.text(script_plan,script_value)
        style = control['style'];alignment = style.get('TextAlignment', 'TopLeft')
        css = {'position': 'absolute', 'box-sizing': 'border-box', 'overflow': 'hidden',
               'left': str(control['x']*mm)+'mm', 'top': str(control['y']*mm)+'mm',
               'width': str(control['width']*mm)+'mm', 'height': str(control['height']*mm)+'mm',
               'white-space': 'pre-wrap', 'display': 'flex',
               'align-items': 'center' if 'Middle' in alignment else 'flex-end' if 'Bottom' in alignment else 'flex-start',
               'justify-content': 'center' if 'Center' in alignment else 'flex-end' if 'Right' in alignment else 'flex-start',
               'text-align': 'center' if 'Center' in alignment else 'right' if 'Right' in alignment else 'left'}
        font = re.fullmatch(r'(.+?),\s*([\d.]+)pt(?:,\s*style=(.*))?', style.get('Font', 'Arial, 10pt'))
        if font:
            css.update({'font-family': font[1], 'font-size': font[2]+'pt',
                        'font-weight': 'bold' if 'Bold' in (font[3] or '') else 'normal',
                        'font-style': 'italic' if 'Italic' in (font[3] or '') else 'normal',
                        'text-decoration': 'underline' if 'Underline' in (font[3] or '') else 'none'})
        for old, new in [('ForeColor', 'color'), ('BackColor', 'background-color')]:
            if style.get(old):css[new] = color(style[old])
        border = float(style.get('BorderWidth', '1'))*mm
        sides = style.get('Borders', 'None')
        for side in ['Left', 'Right', 'Top', 'Bottom']:
            if side in sides or sides == 'All':css['border-'+side.lower()] = str(border)+'mm solid currentColor'
        if control['kind'] == 'XRLine':css['border-top'] = str(float(control['attributes'].get('LineWidth', '1'))*mm)+'mm solid currentColor'
        padding = [float(v) for v in style.get('Padding', '0,0,0,0,100').split(',')]
        if len(padding) == 5:
            l, r, t, b, pdpi = padding
            css['padding'] = ' '.join(str(v*25.4/pdpi)+'mm' for v in [t,r,b,l])
        if control['kind']=='XRBarCode' and control['symbology']['Name']=='Code128':
            from .source_phase6_linear_print import html as linear_html
            content=linear_html(text,control)
        else:content=qr_print.svg(text,control['symbology']) if control['kind']=='XRBarCode' else escape(text)
        extra=''.join(' '+k+'="'+escape(v,quote=True)+'"' for k,v in attributes.items())
        return '<div'+extra+' style="'+escape(';'.join(k+':'+v for k,v in css.items()), quote=True)+'">'+content+'</div>'+''.join(control_html(child,values,scope,page_rows,page_number,page_count) for child in control['children'])

    def band_html(band, values, y, scope=None):
        return (band,values,y,scope)

    row_positions={id(values):index for index,values in enumerate(rows)}
    def finish_page(html, values, page_rows, end_y):
        if page_rows:
            last=row_positions[id(page_rows[-1])]
            repeating=[b for b in sorted(bands['GroupFooterBand'],key=level) if b['attributes'].get('RepeatEveryPage')=='true' and group_rows[last,level(b)][1]>last+1]
            for pos,band in enumerate(repeating):
                if end_y+band['height']>height-bottom-footer_height+1e-6:raise ValidationError({'layout':'重复组尾超过纸张可用高度'})
                if band['attributes'].get('PrintAtBottom')=='true':end_y=max(end_y,height-bottom-footer_height-sum(b['height'] for b in repeating[pos:]))
                html.append(band_html(band,values,end_y,scope_at(last,band)));end_y+=band['height']
        y = height-bottom-footer_height
        for band in bands['PageFooterBand']:
            html.append(band_html(band,values,y));y += band['height']
        for band in bands['TopMarginBand']:html.append(band_html(band,values,0))
        for band in bands['BottomMarginBand']:html.append(band_html(band,values,height-bottom))
        return {'bands':html,'rows':list(page_rows)}

    def scope_at(index,band=None):
        if not headers:return None
        current=level(band) if band is not None else level(headers[-1])
        return rows[slice(*group_rows[index,current])]

    def group_height(index,band):
        start,end=group_rows[index,level(band)]
        total=(end-start)*detail_height
        for pos in range(start,end):
            total+=sum(b['height'] for b in group_starts.get(pos,[]) if level(b)<=level(band))
            total+=sum(b['height'] for b in bands['GroupFooterBand'] if level(b)<=level(band) and level(b) in group_ends.get(pos+1,[]))
        return total

    # 组头从外到内，组尾从内到外；零高度明细仍逐行进入所属组的汇总。
    pages = [];index = 0
    while index < len(rows):
        first = not pages;html = [];page_rows=[];y = top;page_start=index
        header = [*(bands['ReportHeaderBand'] if first else []), *bands['PageHeaderBand']]
        for band in header:
            html.append(band_html(band, rows[index], y));y += band['height']
        limit=height-bottom-footer_height
        while index<len(rows):
            scope=scope_at(index)
            group_headers=[b for b in headers if b in group_starts.get(index,[])
                or index==page_start and b['attributes'].get('RepeatEveryPage')=='true']
            header_height=sum(b['height'] for b in group_headers)
            if index>page_start and any(b['attributes'].get('PageBreak')=='BeforeBand' or
                b['attributes'].get('GroupUnion')=='WholePage' and y+group_height(index,b)>limit+1e-6 for b in group_starts.get(index,[])):break
            ending=sorted([b for b in bands['GroupFooterBand'] if level(b) in group_ends.get(index+1,[])],key=level)
            reserve=sum(b['height'] for b in ending if b['attributes'].get('GroupUnion')=='WithLastDetail')
            reserve+=sum(b['height'] for b in bands['GroupFooterBand'] if b not in ending and b['attributes'].get('RepeatEveryPage')=='true')
            if y+header_height+detail_height+reserve>limit+1e-6:break
            for band in group_headers:
                html.append(band_html(band,rows[index],y,scope_at(index,band)));y+=band['height']
            for band in bands['DetailBand']:
                html.append(band_html(band, rows[index], y,scope));y += band['height']
            page_rows.append(rows[index]);index+=1
            if ending:
                for end_index,band in enumerate(ending):
                    if y+band['height']>limit+1e-6:
                        pages.append(finish_page(html,rows[index-1],page_rows,y));html=[];page_rows=[];y=top;page_start=index-1
                        for header_band in [*bands['PageHeaderBand'],*(b for b in headers if b['attributes'].get('RepeatEveryPage')=='true' and level(b)>=level(band))]:
                            html.append(band_html(header_band,rows[index-1],y,scope_at(index-1,header_band) if header_band['kind']=='GroupHeaderBand' else None))
                            y+=header_band['height']
                    if y+band['height']>limit+1e-6:
                        raise ValidationError({'layout':'原组尾超过一页可用高度。'})
                    if band['attributes'].get('PrintAtBottom')=='true' and band['height']>0:
                        y=max(y,limit-sum(b['height'] for b in ending[end_index:]))
                    html.append(band_html(band,rows[index-1],y,scope_at(index-1,band)));y+=band['height']
        if index==page_start:
            raise ValidationError({'layout': '原页边距、分组及固定明细高度超出纸张；需核实旧裁切/缩放设置。'})
        if index == len(rows):
            for band in bands['ReportFooterBand']:
                if y+band['height'] > height-bottom-footer_height:
                    pages.append(finish_page(html,rows[index-1],page_rows,y));html=[];page_rows=[];y=top
                    for page_header in bands['PageHeaderBand']:
                        html.append(band_html(page_header,rows[index-1],y));y += page_header['height']
                if y+band['height'] > height-bottom-footer_height:
                    raise ValidationError({'layout':'原报表尾部超过一页可用高度。'})
                html.append(band_html(band, rows[index-1], y));y += band['height']
        pages.append(finish_page(html,rows[index-1],page_rows,y))
    rendered_pages=[]
    for number,page in enumerate(pages,1):
        rendered_pages.append(''.join('<div style="position:absolute;left:'+str(left*mm)+'mm;top:'+str(y*mm)+'mm">'+
            ''.join(control_html(c,values,scope,page['rows'],number,len(pages)) for c in band['controls'])+'</div>'
            for band,values,y,scope in page['bands']))
    page_css = f'width:{width*mm}mm;height:{height*mm}mm;'
    html = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>'+escape(str(row['RptTitle']))+'</title><style>@page{size:'+str(width*mm)+'mm '+str(height*mm)+'mm;margin:0}body{margin:0}.page{position:relative;overflow:hidden;break-after:page;'+page_css+'}.page:last-child{break-after:auto}@media screen{body{background:#eee}.page{background:white;margin:8px auto;box-shadow:0 0 3px #999}}</style><body>'+''.join('<section class="page">'+p+'</section>' for p in rendered_pages)+'</body></html>'
    if bookmarks:
        navigation='<nav class="original-bookmarks" aria-label="原报表书签">'+''.join('<a href="#'+b['anchor']+'">'+escape(b['text'] or ('〈NULL〉' if b['is_null'] else '〈空书签〉'))+'（第'+str(b['page'])+'页）</a> ' for b in bookmarks)+'</nav>'
        html=html.replace('<body>','<body><style>@media print{.original-bookmarks{display:none}}.original-bookmarks{padding:8px}</style>'+navigation,1)
    return {'report_id': row['RptID'], 'title': row['RptTitle'], 'template_sha256': layout['sha256'],
            'entry': entry, 'record_count': len(result['rows']), 'page_count': len(pages), 'html': html, 'generated_at':generated_at.isoformat(),
            'mode': 'original_bound_proof', 'historical_reconciliation': '未完成', 'field_acceptance': '待纸张、字体、打印机验收',
            'reference_resolutions': result.get('reference_resolutions', []),'period':result.get('period'),'print_selection':result.get('print_selection'),
            'parent_source_resolutions':result.get('parent_source_resolutions',[]),'metadata_bindings':metadata_bindings,'bookmarks':bookmarks,
            'text_script':None if script_plan is None else {'control':script_plan[1],'event':script_plan[2],'inputs':script_plan[4]},
            'calculated_fields':result.get('calculated_fields',[]),
            'calculation_usage': calculation_usage(parse_xml(base64.b64decode(row['TemplateXml']))[0]),
            'formatting_usage': formatting_usage(root),
            'notes': [*([PROJECTION_NOTES[entry]] if entry in PROJECTION_NOTES else []),'已支持逐行算术、条件/逻辑、Abs、IsNull、Round、字符串及日期函数；原版本NULL/舍入/类型细节仍待同值对账，除零或缺来源不会跳过原行。', '页汇总只包含该页实际明细；页码在分页后填入。无显式格式的日期采用yyyy-MM-dd HH:mm:ss，默认总页码采用当前页 / 总页数，旧客户端文化格式待核对。', '固定高度原版式填数校样；未调用打印前业务动作，不增加打印次数，不表示设备已成功打印。',
                      '缺客户端枚举时明确显示原代码；资料代码对应多个名称时全部列出候选。此类显示属于明确替代，不计作原模板完整复刻。',
                      *(['Code128采用原字符集（省略时A）、校验位与自动模块；完整内容不截断。多选机台串暂按完整原代码显示。条码静区、字体及旧打印机可扫性仍待原成品对照。'] if any(n.get('Name')=='Code128' for n in root.findall('.//Symbology')) else []),
                      *(['未定义组头的组尾以整份所选单据为范围，按Level从内到外输出；不改原XML。该规则及跨页校样已实现，原12.2客户端同值样张待对照。'] if not bands['GroupHeaderBand'] and bands['GroupFooterBand'] else []),
                      *(['分组按原Level从外到内，组尾同Level对应；支持零高度明细、组前分页、WholePage、重复组头和组汇总；文本采用Unicode排序，旧区域排序仍待核对。'] if group_starts else [])]}
