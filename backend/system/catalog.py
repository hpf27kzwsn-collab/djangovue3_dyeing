from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, ClockedSchedule, SolarSchedule
from django_celery_results.models import TaskResult
from . import models
from .model_catalog import project_models

ENTITIES = {
    'user': models.Users, 'dept': models.Dept, 'post': models.Post, 'role': models.Role,
    'menu': models.Menu, 'menu_button': models.MenuButton, 'column': models.MenuField,
    'role_menu_permission': models.RoleMenuPermission, 'role_menu_button_permission': models.RoleMenuButtonPermission,
    'field_permission': models.FieldPermission, 'api_white_list': models.ApiWhiteList,
    'dictionary': models.Dictionary, 'area': models.Area, 'system_config': models.SystemConfig,
    'file': models.FileList, 'operation_log': models.OperationLog, 'login_log': models.LoginLog,
    'message_center': models.MessageCenter, 'download_center': models.DownloadCenter,
    'periodic_task': PeriodicTask, 'interval_schedule': IntervalSchedule, 'crontab_schedule': CrontabSchedule,
    'clocked_schedule': ClockedSchedule, 'solar_schedule': SolarSchedule, 'task_result': TaskResult,
}

ENTITIES.update({f'{model._meta.app_label}_{model._meta.model_name}': model for model in project_models()
                 if model._meta.app_label != 'system' and model not in ENTITIES.values()})

HIDDEN_ENTITIES = {'menu_button', 'column', 'role_menu_permission', 'role_menu_button_permission', 'field_permission',
                   'interval_schedule', 'crontab_schedule', 'clocked_schedule', 'solar_schedule'}
