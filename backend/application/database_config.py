"""源码服务和管理命令共用的数据库配置。"""
import os
from configparser import ConfigParser
from pathlib import Path


def config_path(base_dir):
    return Path(os.environ.get('DJANGO_DATABASE_CONFIG', Path(base_dir).parent / 'database.ini'))


def read_config(base_dir, path=None):
    config = ConfigParser(interpolation=None)
    config.read(path or config_path(base_dir), encoding='utf-8-sig')
    return config


def database_settings(base_dir, path=None, use_environment=True):
    config = read_config(base_dir, path)

    def value(section, key, env, default=None):
        result = os.environ.get(env) if use_environment else None
        if result is None:
            result = config.get(section, key, fallback=default)
        if result is None:
            raise ValueError(f'数据库配置缺少 {section}.{key}（{env}）')
        return result

    engine = value('database', 'engine', 'DJANGO_DB_ENGINE', 'sqlite')
    if engine == 'sqlite':
        path = Path(value('sqlite', 'path', 'DJANGO_SQLITE_PATH', 'db.sqlite3'))
        return {'ENGINE': 'django.db.backends.sqlite3',
                'NAME': path if path.is_absolute() else Path(base_dir) / path,
                'OPTIONS': {'transaction_mode': 'IMMEDIATE'}}
    if engine == 'postgresql':
        return {'ENGINE': 'django.db.backends.postgresql',
                'NAME': value('postgresql', 'name', 'DJANGO_DB_NAME'),
                'USER': value('postgresql', 'user', 'DJANGO_DB_USER'),
                'PASSWORD': value('postgresql', 'password', 'DJANGO_DB_PASSWORD'),
                'HOST': value('postgresql', 'host', 'DJANGO_DB_HOST', '127.0.0.1'),
                'PORT': value('postgresql', 'port', 'DJANGO_DB_PORT', '5432'),
                'OPTIONS': {'sslmode': value('postgresql', 'sslmode', 'DJANGO_DB_SSLMODE', 'prefer')}}
    raise ValueError(f'数据库类型 {engine!r} 不在本框架的 sqlite/postgresql 配置中')


def write_config(base_dir, engine, sqlite_path, postgresql, path=None):
    path = Path(path or config_path(base_dir))
    config = read_config(base_dir, path)
    config['database'] = {'engine': engine}
    config['sqlite'] = {'path': str(sqlite_path)}
    config['postgresql'] = postgresql
    with path.open('w', encoding='utf-8') as stream:
        config.write(stream)
    return path
