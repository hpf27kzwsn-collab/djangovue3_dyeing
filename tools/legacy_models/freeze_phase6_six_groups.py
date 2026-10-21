"""固定六组续项基线；编号按原顺序保留重复配置，不把交叉统计相加。"""
import json,hashlib
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/erp-phase6-six-groups-baseline-20261017.json'

def read(name):return json.loads((ROOT/'docs'/name).read_text(encoding='utf8'))

def main():
    if OUT.exists():
        print('沿用已固定基线：'+str(OUT));return
    formulas=read('erp-phase6-entry-formula-audit-20261017.json')
    hooks=read('erp-phase6-hook-review-20261016.json')
    runtime=read('erp-phase6-runtime-review-20261017.json')
    layouts=read('erp-phase6-layout-review-20261017.json')
    previous=read('erp-phase6-service-values-verification-20261017.json')
    groups={str(n):[] for n in range(1,7)}
    for index,row in enumerate(formulas['outside_registry_followup'],1):
        group={'本行或SQL函数公式':'1','父子来源公式':'2','未绑定模型':'3','非物理目标':'3'}[row['category']]
        groups[group].append({'id':f'F{index:03}',**row})
    for prefix,rows in [('H',hooks['bindings']),('C',runtime['field_copy_rows']),('L',runtime['context_filters'])]:
        groups['4'].extend({'id':f'{prefix}{n:03}','configuration':row} for n,row in enumerate(rows,1))
    groups['5']=[{'id':f'P{n:03}','configuration':row} for n,row in enumerate(layouts['reports'],1)]
    groups['6']=[{'id':'V001','task':'逐规则必要非空、异常、重复、NULL和负数回归'},
                 {'id':'V002','task':'新保存及父子链、转单逆向、显示/打印的浏览器验证'},
                 {'id':'V003','task':'模型字段、迁移、前端及文档数量一致性'},
                 {'id':'V004','task':'历史对账与现场验收独立登记'}]
    names=['erp-phase6-entry-formula-audit-20261017.json','erp-phase6-hook-review-20261016.json','erp-phase6-runtime-review-20261017.json','erp-phase6-layout-review-20261017.json']
    result={'frozen_at':datetime.now().astimezone().isoformat(),'scope':'六组连续推进；财务暂缓；35查询暂缓；原配置不去重',
        'groups':groups,'counts':{k:len(v) for k,v in groups.items()},'paused_queries':previous['paused_nonfinancial_queries'],
        'source_hashes':{name:hashlib.sha256((ROOT/'docs'/name).read_bytes()).hexdigest() for name in names},
        'note':'编号仅表示固定核验单元；不同组交叉，不能相加当作未开发功能数。现有130条统一保存公式保留在基线来源中，不重复列新增。'}
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(result['counts'])

if __name__=='__main__':main()
