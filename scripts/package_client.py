"""生成仅含客户运行代码与已构建前端的交付目录，不带旧库提取/开发资料。"""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def package(destination):
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(ROOT / 'backend', destination / 'backend', ignore=shutil.ignore_patterns(
        '__pycache__', '*.pyc', 'tests', 'test*.py', 'staticfiles', 'media', '*.sqlite3', '*.log',
        'examples', 'generate_crud.py',
        'source_phase6_templates.json.gz', 'source_phase6_layout_manifest.json'))
    shutil.copytree(ROOT / 'web/dist', destination / 'web/dist')
    shutil.copy(ROOT / 'docs/客户ERP独立部署与资料导入.md', destination / '使用说明.md')
    (destination / 'database.ini.example').write_text(
        '[database]\nengine = postgresql\n\n[postgresql]\n'
        'name = customer_erp\nuser = customer_erp\npassword = 请填写客户数据库密码\n'
        'host = 127.0.0.1\nport = 5432\nsslmode = prefer\n', encoding='utf-8')
    print(destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    package(parser.parse_args().destination.resolve())
