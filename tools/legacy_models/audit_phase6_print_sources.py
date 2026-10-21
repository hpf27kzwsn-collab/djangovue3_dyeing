"""133份非财务打印的原XML与C#模板逐份来源复查；只分析，不执行原脚本。"""
import os,sys,json,base64,re,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','application.settings')
import django
django.setup()
from plugins.erp_base.source_phase6_api import templates
from plugins.erp_base.source_phase6_layouts import parse_xml,kind
from plugins.erp_base.source_phase6_rendering import requirements


def digest(value):return hashlib.sha256(value).hexdigest()


def executable_text(value):
    # 方法声明不能从注释或赋给 ScriptsSource 的字符串重复认领。
    return re.sub(r'@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*.*?\*/|//[^\r\n]*',
                  ' ',value,flags=re.S)


def main():
    prior=json.loads((ROOT/'docs/erp-phase6-print-source-baseline-20261018.json').read_text(encoding='utf8'))
    reports={r['RptID']:r for r in templates()};rows=[]
    for item in prior['rows']:
        report=reports[item['report']];xml=base64.b64decode(report['TemplateXml']);root,_=parse_xml(xml)
        template=base64.b64decode(report['Template']) if report['Template'] else b''
        source=template.decode('utf-8-sig')
        scripts='\n'.join(n.get('ScriptsSource','')+'\n'+n.get('ScriptSource','') for n in root.iter())
        script_code=executable_text(scripts);template_code=executable_text(source)
        events=[]
        for node in root.iter():
            config=node.find('Scripts')
            if config is None:continue
            for event,method in config.attrib.items():
                if event=='Ref':continue
                pattern=r'\b(?:void|bool|string|int|object)\s+'+re.escape(method)+r'\s*\('
                events.append({'control':node.get('Name'), 'event':event,'method':method,
                    'xml_method_declaration':bool(re.search(pattern,script_code)),
                    'template_method_declaration':bool(re.search(pattern,template_code))})
        rows.append({'id':item['id'],'report':item['report'],'title':report['RptTitle'],'entry':root.get('DataMember'),
            'xml_sha256':digest(xml),'template_sha256':digest(template),'template_bytes':len(template),
            'prior_issues':item['issues'],'current_issues':requirements(report),'script_events':events,
            'scripts_source_nonempty':bool(scripts.strip()),
            'missing_script_definitions':[e['method'] for e in events if not e['xml_method_declaration'] and not e['template_method_declaration']],
            'development':'已有可执行内容继续逐项开发；仅解析或找到方法声明不代表实现',
            'historical_reconciliation':'未完成','field_acceptance':'未完成'})
    assert len(rows)==133
    evidence={'scope':'本轮开始时133份非财务打印差异，固定编号不删减；原35查询与财务继续暂缓',
        'reports_checked':len(rows),'reports_with_script_events':sum(bool(r['script_events']) for r in rows),
        'reports_with_missing_script_definitions':sum(bool(r['missing_script_definitions']) for r in rows),
        'reports_with_scripts_source':sum(r['scripts_source_nonempty'] for r in rows),
        'remaining_report_count':sum(bool(r['current_issues']) for r in rows),
        'script_method_note':'排除C#注释和字符串后匹配方法声明，用于定位来源，未执行或验证原脚本；无声明也可能依赖未提供客户端程序集，不能视为空事件。',
        'rows':rows}
    (ROOT/'docs/erp-phase6-print-source-audit-20261018.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    text='# 第六阶段133份非财务打印原来源复查\n\n逐份读取原XML和原C#模板，未执行脚本。范围固定为本轮开始时133份差异；此前25份可校样不重复计算。\n\n'
    text+=f"共复查133份；{evidence['reports_with_script_events']}份含事件名，{evidence['reports_with_missing_script_definitions']}份存在XML和C#模板都未找到方法声明的事件；{evidence['reports_with_scripts_source']}份包含脚本文本。现有代码补齐后，本批剩余{evidence['remaining_report_count']}份差异。方法声明存在也不等于已移植；缺失的需要原客户端实现，不按空事件跳过。\n\n"
    text+='开发、历史全量对账、现场验收分别登记；本表是来源复查，不能视为133份开发完成。原35查询、财务继续暂缓。\n\n|固定编号|报表|原入口|仍缺功能/来源|未找到定义的原事件函数|\n|---|---|---|---|---|\n'
    for r in rows:
        values=[r['id'],r['report']+' '+r['title'],r['entry'],'；'.join(r['current_issues']) or '已具备静态校样条件，实际验证见六组清单','；'.join(r['missing_script_definitions']) or '无缺失声明记录（不代表脚本已实现）']
        text+='|'+'|'.join(str(v).replace('|','\\|').replace('\n','<br>') for v in values)+'|\n'
    text+='\n原XML与模板逐份哈希、事件绑定、声明定位和前后问题列表见[JSON证据](erp-phase6-print-source-audit-20261018.json)。\n'
    (ROOT/'docs/2026-10-18第六阶段133份非财务打印来源复查.md').write_text(text,encoding='utf8')
    print({k:v for k,v in evidence.items() if k!='rows'})

if __name__=='__main__':main()
