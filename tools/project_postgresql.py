"""按本项目配置启动本地开发PostgreSQL；相对数据目录跟随项目根目录。"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from application.database_config import read_config, database_settings


def start():
    config = read_config(ROOT / 'backend')
    if not config.has_section('local_postgresql') or not config.getboolean('local_postgresql', 'manage'):
        return
    database = database_settings(ROOT / 'backend')
    if database['ENGINE'] != 'django.db.backends.postgresql' or database['HOST'] not in ('127.0.0.1', 'localhost'):
        return
    if str(database['PORT']) != config.get('local_postgresql', 'port'):
        return
    data = (ROOT / config.get('local_postgresql', 'data_directory')).resolve()
    executable = Path(config.get('local_postgresql', 'bin_directory')) / 'pg_ctl.exe'
    process_options = {'creationflags': subprocess.CREATE_NO_WINDOW} if sys.platform == 'win32' else {}
    status = subprocess.run([str(executable), 'status', '-D', str(data)], capture_output=True, **process_options)
    if status.returncode == 3:
        subprocess.run([str(executable), 'start', '-w', '-D', str(data), '-l', str(data.parent / 'project-postgresql.log'),
            '-o', '-p ' + str(database['PORT']) + ' -h 127.0.0.1 -c max_locks_per_transaction=1024'], check=True, **process_options)
    elif status.returncode != 0:
        raise subprocess.CalledProcessError(status.returncode, status.args, output=status.stdout, stderr=status.stderr)
    import psycopg
    with psycopg.connect(dbname=database['NAME'], user=database['USER'], password=database['PASSWORD'],
        host=database['HOST'], port=database['PORT'], **database['OPTIONS']) as connection:
        actual = Path(connection.execute('SHOW data_directory').fetchone()[0]).resolve()
    if actual != data:
        raise ValueError('当前端口连接的数据目录与本项目配置不同，请为复制后的项目配置独立端口。')
    print('本项目开发数据库已就绪。')


if __name__ == '__main__':
    start()
