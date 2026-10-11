import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from django.db import connection
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient
from django.core.management import call_command
from application.database_config import database_settings, write_config
from system.models import Users, Post


class DatabaseConfigurationTests(SimpleTestCase):
    def test_default_sqlite_and_explicit_postgresql_are_separate(self):
        with TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True):
            base = Path(directory) / 'backend'
            self.assertEqual(database_settings(base)['NAME'], base/'db.sqlite3')
            path = Path(directory)/'database.ini'
            values = {'name':'erp','host':'127.0.0.1','port':'55432','user':'erp','password':'50%中文!','sslmode':'prefer'}
            write_config(base, 'postgresql', 'db.sqlite3', values, path)
            result = database_settings(base)
            self.assertEqual((result['ENGINE'],result['PASSWORD']), ('django.db.backends.postgresql','50%中文!'))
            self.assertNotIn('transaction_mode',result['OPTIONS'])
            write_config(base,'sqlite','other.sqlite3',values,path)
            self.assertEqual(database_settings(base)['NAME'],base/'other.sqlite3')

    def test_environment_overrides_file_but_transfer_uses_explicit_file(self):
        with TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True):
            path = Path(directory)/'database.ini'
            base = Path(directory)/'backend'
            write_config(base,'sqlite','original.sqlite3',{},path)
            with patch.dict(os.environ, {'DJANGO_SQLITE_PATH':'environment.sqlite3'}):
                self.assertEqual(database_settings(base)['NAME'],base/'environment.sqlite3')
                self.assertEqual(database_settings(base,path,use_environment=False)['NAME'],base/'original.sqlite3')

    def test_selected_postgresql_does_not_fall_back_to_sqlite(self):
        with TemporaryDirectory() as directory, patch.dict(os.environ, {'DJANGO_DB_ENGINE':'postgresql'}, clear=True):
            with self.assertRaisesRegex(ValueError,'postgresql.name'):
                database_settings(Path(directory))

    def test_fixture_loading_does_not_publish_live_notifications(self):
        from types import SimpleNamespace
        from system.signals import receipt_changed
        with patch('system.signals.notify_users') as notify:
            receipt_changed(None,SimpleNamespace(users_id=7),raw=True)
            notify.assert_not_called()
            receipt_changed(None,SimpleNamespace(users_id=7),raw=False)
            notify.assert_called_once_with([7])


class DatabaseBackendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data',verbosity=0)

    def test_readiness_and_list_with_backend_without_parameter_cap(self):
        client = APIClient()
        client.force_authenticate(Users.objects.get(username='superadmin'))
        self.assertEqual(client.get('/readiness').json()['database'],connection.vendor)
        Post.objects.create(name='无参数上限',code='no-cap')
        with patch.object(connection.features,'max_query_params',None):
            response = client.get('/api/system/post/')
            self.assertEqual(response.status_code,200)
            self.assertIn('no-cap',[row['code'] for row in response.data['data']])
        Post.objects.all().delete()
        with patch.object(connection.features,'max_query_params',None):
            self.assertEqual(client.get('/api/system/post/').data['data'],[])
