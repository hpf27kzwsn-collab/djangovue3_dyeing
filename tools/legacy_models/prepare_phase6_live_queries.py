"""为旧库只读结果集描述生成55项原SELECT；本工具不连接数据库。"""
import argparse
import gzip
import json
from pathlib import Path
from sqlglot import exp,parse_one

ROOT=Path(__file__).resolve().parents[2]


def prepare(directory):
    base=ROOT/'backend/plugins/erp_base'
    catalog=json.loads(gzip.decompress((base/'source_phase6_catalog.json.gz').read_bytes()))
    support=json.loads((base/'source_phase6_query_support.json').read_text(encoding='utf8'))
    queries=[]
    for row in catalog['entries']:
        name=row['table']['DataTableName']
        if support[name]['query_state']!='unresolved':continue
        tree=parse_one(row['table']['SQL'],read='tsql')
        assert isinstance(tree,exp.Query),name
        for parameter in list(tree.find_all(exp.Parameter)):parameter.replace(exp.Null())
        ctes={node.alias.lower() for node in tree.find_all(exp.CTE)}
        for table in tree.find_all(exp.Table):
            if not table.db and not table.catalog and table.name.lower() not in ctes:
                table.set('db',exp.to_identifier('dye'))
        queries.append({'name':name,'sql':tree.sql(dialect='tsql')})
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'queries.json').write_text(json.dumps(queries,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print({'queries':len(queries),'mode':'SELECT metadata input only'})


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-directory',type=Path,required=True)
    prepare(parser.parse_args().output_directory)
