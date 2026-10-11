"""配置入口共用的 PostgreSQL 连通性及首次建库操作。"""
def connection_options(values):
    return {key: values[key] for key in ['host', 'port', 'user', 'password', 'sslmode']} | {'dbname': values['name']}


def test_postgresql(values):
    import psycopg
    with psycopg.connect(**connection_options(values)) as connection:
        return connection.execute('SELECT version()').fetchone()[0]


def create_postgresql(values, admin_user, admin_password):
    import psycopg
    from psycopg import sql
    options = connection_options(values) | {'dbname': 'postgres', 'user': admin_user, 'password': admin_password}
    with psycopg.connect(**options, autocommit=True) as connection:
        if not connection.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', (values['user'],)).fetchone():
            connection.execute(sql.SQL('CREATE ROLE {} LOGIN PASSWORD {}').format(
                sql.Identifier(values['user']), sql.Literal(values['password'])))
        if not connection.execute('SELECT 1 FROM pg_database WHERE datname=%s', (values['name'],)).fetchone():
            connection.execute(sql.SQL('CREATE DATABASE {} OWNER {} ENCODING \'UTF8\'').format(
                sql.Identifier(values['name']), sql.Identifier(values['user'])))
    return test_postgresql(values)
