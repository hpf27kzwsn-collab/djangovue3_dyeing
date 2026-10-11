"""源码版配置/连通性/建库/初始化统一入口；密码通过终端隐藏输入。"""
import argparse
import getpass
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(os.environ.get('DJANGO_BASE_DIR', ROOT / 'backend'))
sys.path.insert(0, str(ROOT / 'backend'))
from application.database_config import database_settings, read_config, write_config
from application.database_tools import create_postgresql, test_postgresql


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    sqlite = commands.add_parser('sqlite', help='选择 SQLite；不会搬迁已有数据')
    sqlite.add_argument('--path', default='db.sqlite3')
    pg = commands.add_parser('postgresql', help='连接 PostgreSQL 并保存配置；不会搬迁已有数据')
    pg.add_argument('--host', default='127.0.0.1')
    pg.add_argument('--port', default='5432')
    pg.add_argument('--name', default='djangovue3')
    pg.add_argument('--user', default='djangovue3')
    pg.add_argument('--sslmode', default='prefer')
    pg.add_argument('--create-database', action='store_true', help='使用管理员创建应用账号及数据库；已有账号不改密码')
    pg.add_argument('--admin-user', default='postgres')
    commands.add_parser('show', help='显示当前连接目标，不显示密码')
    commands.add_parser('initialize', help='对当前所选数据库迁移并初始化菜单/区域')
    args = parser.parse_args()
    if args.action == 'show':
        values = database_settings(BASE)
        print(json.dumps({key:str(value) for key,value in values.items() if key in ['ENGINE','NAME','HOST','PORT','USER']}, ensure_ascii=False, indent=2))
    elif args.action == 'initialize':
        for command in ['migrate', 'init_data', 'init_area']:
            subprocess.run([sys.executable, str(ROOT/'backend'/'manage.py'), command], check=True)
    else:
        config = read_config(BASE)
        values = dict(config['postgresql']) if config.has_section('postgresql') else {}
        sqlite_path = config.get('sqlite', 'path', fallback='db.sqlite3')
        if args.action == 'postgresql':
            values = {key:getattr(args,key) for key in ['host','port','name','user','sslmode']}
            values['password'] = getpass.getpass('应用账号密码：')
            if args.create_database:
                create_postgresql(values, args.admin_user, getpass.getpass('PostgreSQL 管理员密码：'))
            else:
                test_postgresql(values)
        else:
            sqlite_path = args.path
        path = write_config(BASE, args.action, sqlite_path, values)
        print(f'配置已保存：{path}。重启网页、worker、beat 后生效；已有数据不会自动搬迁。')


if __name__ == '__main__':
    main()
