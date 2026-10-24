from django.db import models, transaction
from django.apps import apps
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from core.api import ModelViewSet, serializer_for, success, AUDIT_FIELDS
from core.permissions import field_access, scoped_queryset, ApiPermission
from .catalog import ENTITIES
from .models import *
from .serializers import UserSerializer, FileSerializer, DeptSerializer, AreaSerializer, MenuSerializer, RoleSerializer, MenuFieldSerializer, ConfigSerializer, DictionarySerializer
from .actions import resource_actions, workflow_actions
from .dictionaries import dictionary_value, dictionary_key, dictionary_options
from core.resources import resource_options
from .model_catalog import permission_models
from .notifications import notify_users
from core.responses import Pagination
from .auth import config
from .excel import ExcelActions
from types import SimpleNamespace
from copy import copy
from django.utils.module_loading import import_string
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiTypes
from django_celery_beat.models import PeriodicTask
import json


class ResourceViewSet(ExcelActions, ModelViewSet):
    lookup_value_regex = r'\d+'
    @classmethod
    def get_extra_actions(cls):
        return [method for method in super().get_extra_actions() if method.__name__ != 'init_data']

    @action(methods=['get'], detail=False)
    def tree(self, request):
        return success(self.get_serializer(self.filter_queryset(self.get_queryset()), many=True).data)

    @action(methods=['put'], detail=False)
    @transaction.atomic
    def batch_update(self, request):
        audit = self.audit()
        audit.pop('creator', None)
        audit.pop('dept_belong_id', None)
        for row in request.data:
            instance = self.get_queryset().get(pk=row[self.queryset.model._meta.pk.name])
            serializer = self.get_serializer(instance, data=row, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(**audit)
        return success(msg='批量更新成功')


class UserViewSet(ResourceViewSet):
    queryset = Users.objects.exclude(is_superuser=True).select_related('creator', 'dept').prefetch_related('role', 'post').order_by('-pk')
    serializer_class = UserSerializer
    search_fields = ['username', 'name', 'dept__name', 'role__name']

    def filter_queryset(self, queryset):
        if self.request.query_params.get('include_children') == 'true' and self.request.query_params.get('dept'):
            departments = department_ids(int(self.request.query_params['dept']))
            request = copy(self.request)
            request._request = copy(self.request._request)
            request._request.GET = self.request.query_params.copy()
            del request._request.GET['dept']
            self.request = request
            queryset = queryset.filter(dept_id__in=departments)
        return super().filter_queryset(queryset)

    @action(methods=['post'], detail=True)
    def reset_password(self, request, pk=None):
        if not request.user.is_superuser:
            raise PermissionDenied('只允许超级管理员重置密码')
        user = self.get_object()
        password = serializers.CharField(trim_whitespace=False).run_validation(request.data['password'])
        if request.data['password'] != request.data['password_confirm']:
            raise serializers.ValidationError('两次密码不匹配')
        user.set_password(password)
        user.save(update_fields=['password'])
        return success(msg='密码已重置')

    @action(methods=['put'], detail=True)
    def reset_to_default_password(self, request, pk=None):
        if not request.user.is_superuser:
            raise PermissionDenied('只允许超级管理员重置密码')
        user = self.get_object()
        user.set_password(config('base.default_password', 'admin123456'))
        user.save(update_fields=['password'])
        return success(msg='已恢复默认密码')


class MenuFieldViewSet(ResourceViewSet):
    queryset = MenuField.objects.select_related('creator').order_by('model', 'id')
    serializer_class = MenuFieldSerializer

    @action(methods=['get'], detail=False)
    def get_models(self, request):
        return success([{'app': model._meta.app_label, 'title': str(model._meta.verbose_name), 'key': model._meta.label,
                         'entity':next((name for name, value in ENTITIES.items() if value is model), None)}
                        for model in permission_models()])

    @action(methods=['post'], detail=False)
    @transaction.atomic
    def auto_match_fields(self, request):
        menu = Menu.objects.get(pk=request.data['menu'])
        model = next((model for model in permission_models() if model._meta.label == request.data['model']), None)
        if model is None:
            raise serializers.ValidationError({'model': '模型不存在或不在字段配置目录'})
        for field in model._meta.fields:
            MenuField.objects.get_or_create(menu=menu, model=model._meta.label, field_name=field.name,
                                           defaults={'title': str(field.verbose_name), **self.audit()})
        return success(msg='字段匹配完成')


def department_ids(pk):
    ids, children = [pk], [pk]
    while children:
        children = list(Dept.objects.filter(parent_id__in=children).values_list('pk', flat=True))
        ids.extend(children)
    return ids


class OrderedTreeViewSet(ResourceViewSet):
    queryset = Dept.objects.select_related('creator').order_by('sort', 'pk')
    serializer_class = DeptSerializer

    @transaction.atomic
    def move(self, direction):
        item = self.get_queryset().get(pk=self.request.data['id'])
        siblings = self.get_queryset().filter(parent=item.parent)
        neighbor = siblings.filter(sort__lt=item.sort).order_by('-sort','pk').first() if direction == -1 else siblings.filter(sort__gt=item.sort).order_by('sort','pk').first()
        if neighbor:
            item.sort, neighbor.sort = neighbor.sort, item.sort
            item.save(update_fields=['sort'])
            neighbor.save(update_fields=['sort'])
        return success(msg='排序已更新')

    @action(methods=['post'], detail=False)
    def move_up(self, request):
        return self.move(-1)

    @action(methods=['post'], detail=False)
    def move_down(self, request):
        return self.move(1)


class DeptViewSet(OrderedTreeViewSet):
    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def options(self, request):
        return success(list(Dept.objects.order_by('sort', 'pk').values('id', 'name', 'parent_id', 'status')))

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def info(self, request, pk=None):
        department = get_object_or_404(Dept, pk=pk)
        ids = department_ids(department.pk) if request.query_params.get('include_children') == 'true' else [department.pk]
        query_request = SimpleNamespace(user=request.user, method='GET', path='/api/system/user/')
        users = scoped_queryset(Users.objects.all(), query_request)
        members = users.filter(dept_id__in=ids)
        children = Dept.objects.filter(parent=department)
        return success({'name':department.name, 'owner':department.owner, 'description':department.description,
                        'count':members.count(), 'gender':{str(value):members.filter(gender=value).count() for value in [0,1,2]},
                        'children':[{'id':child.pk, 'name':child.name,
                                     'count':users.filter(dept_id__in=department_ids(child.pk)).count()} for child in children]})


class MenuViewSet(OrderedTreeViewSet):
    queryset = Menu.objects.select_related('creator').order_by('sort', 'pk')
    serializer_class = MenuSerializer


class MenuButtonViewSet(ResourceViewSet):
    queryset = MenuButton.objects.select_related('creator').order_by('name', 'pk')
    serializer_class = serializer_for(MenuButton)

    @action(methods=['post'], detail=False)
    @transaction.atomic
    def batch_create(self, request):
        menu = Menu.objects.get(pk=request.data['menu'])
        entity = request.data.get('entity', menu.resource)
        if entity not in ENTITIES:
            raise serializers.ValidationError({'entity':'请指定已登记的资源实体键'})
        menu.resource = entity
        menu.modifier = request.user
        menu.save(update_fields=['resource', 'modifier', 'update_datetime'])
        actions = resource_actions(entity, view_for(entity, ENTITIES[entity]))
        buttons = []
        for key, title, method, api in actions:
            values = {'menu':menu,'name':title,'method':method,'api':api}
            button, created = MenuButton.objects.get_or_create(value=f'{menu.component_name}:{key}', defaults=values|self.audit())
            if not created:
                for name, value in values.items():
                    setattr(button, name, value)
                button.modifier = request.user
                button.save(update_fields=list(values)+['modifier','update_datetime'])
            buttons.append(button)
        return success(self.get_serializer(buttons, many=True).data, '批量创建完成')


class DictionaryViewSet(ResourceViewSet):
    queryset = Dictionary.objects.select_related('creator').order_by('sort', 'pk')
    serializer_class = DictionarySerializer

    def get_queryset(self):
        rows = super().get_queryset()
        if self.action == 'list' and not self.request.query_params.get('parent'):
            rows = rows.filter(parent__isnull=True)
        return rows


class PeriodicViewSet(ResourceViewSet):
    queryset = PeriodicTask.objects.order_by('-pk')
    serializer_class = serializer_for(PeriodicTask)
    serializer_class.Meta.exclude = ['solar']

    @action(methods=['post'], detail=True)
    def run(self, request, pk=None):
        from application.celery import app
        task = self.get_object()
        result = app.send_task(task.task, args=json.loads(task.args), kwargs=json.loads(task.kwargs))
        return success({'task_id':result.id},'任务已提交')


class RoleViewSet(ResourceViewSet):
    queryset = Role.objects.select_related('creator').order_by('sort', 'pk')
    serializer_class = RoleSerializer

    @action(methods=['get', 'put'], detail=True)
    @transaction.atomic
    def users(self, request, pk=None):
        role = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(request, role)
        query_request = SimpleNamespace(user=request.user, method='GET', path='/api/system/user/')
        users = scoped_queryset(Users.objects.exclude(is_superuser=True).select_related('dept').prefetch_related('role','post'), query_request)
        if request.method == 'PUT':
            ids = set(request.data['ids'])
            operation = request.data.get('operation', 'set')
            if operation not in ['add','remove','set']:
                raise serializers.ValidationError({'operation':'请选择 add、remove 或 set'})
            for user_id in ids:
                get_object_or_404(users, pk=user_id)
            targets = users.filter(Q(pk__in=ids)|Q(role=role)).distinct() if operation == 'set' else users.filter(pk__in=ids)
            for user in targets:
                roles = list(user.role.exclude(pk=role.pk).values_list('pk', flat=True))
                if operation == 'add' or operation == 'set' and user.pk in ids:
                    roles.append(role.pk)
                serializer = UserSerializer(user, data={'role':roles}, partial=True, context={'request':request})
                serializer.is_valid(raise_exception=True)
                serializer.save(modifier=request.user)
            return success(msg='用户授权已更新')
        users = users.filter(role=role) if request.query_params.get('authorized','1') == '1' else users.exclude(role=role)
        if request.query_params.get('name'):
            users = users.filter(Q(name__icontains=request.query_params['name'])|Q(username__icontains=request.query_params['name']))
        if request.query_params.get('dept'):
            users = users.filter(dept_id=request.query_params['dept'])
        page = self.paginate_queryset(users.order_by('pk'))
        return self.get_paginated_response(UserSerializer(page, many=True, context={'request':request}).data)

    @action(methods=['get', 'put'], detail=True)
    @transaction.atomic
    def permissions(self, request, pk=None):
        role = self.get_object()
        if request.method == 'PUT':
            RoleMenuPermission.objects.filter(role=role).exclude(menu_id__in=request.data['menus']).delete()
            for menu_id in request.data['menus']:
                RoleMenuPermission.objects.get_or_create(role=role, menu_id=menu_id, defaults=self.audit())
            RoleMenuButtonPermission.objects.filter(role=role).exclude(menu_button_id__in=[row['id'] for row in request.data['buttons']]).delete()
            for row in request.data['buttons']:
                grant, _ = RoleMenuButtonPermission.objects.get_or_create(role=role, menu_button_id=row['id'], defaults={'data_range':row['data_range'], **self.audit()})
                departments_changed = set(grant.dept.values_list('pk',flat=True)) != set(row['dept'])
                if grant.data_range != row['data_range'] or departments_changed:
                    grant.data_range = row['data_range']
                    grant.modifier = request.user
                    grant.save(update_fields=['data_range','modifier','update_datetime'])
                grant.dept.set(row['dept'])
            FieldPermission.objects.filter(role=role).exclude(field_id__in=[row['id'] for row in request.data['fields']]).delete()
            for row in request.data['fields']:
                grant, _ = FieldPermission.objects.get_or_create(role=role, field_id=row['id'], defaults={key:row[key] for key in ['is_query','is_create','is_update']}|self.audit())
                changed = [key for key in ['is_query','is_create','is_update'] if getattr(grant,key) != row[key]]
                if changed:
                    for key in changed:
                        setattr(grant,key,row[key])
                    grant.modifier = request.user
                    grant.save(update_fields=changed+['modifier','update_datetime'])
        available_buttons = list(MenuButton.objects.values('id', 'name', 'menu_id', 'api', 'method'))
        actor_grants = RoleMenuButtonPermission.objects.filter(role__users=request.user, role__status=True).prefetch_related('dept')
        allowed = {}
        for grant in actor_grants:
            allowed.setdefault(grant.menu_button_id, set()).update(dept.pk for dept in grant.dept.all())
        for button in available_buttons:
            button['assignable_departments'] = None if request.user.is_superuser else sorted(allowed.get(button['id'], set()))
        return success({'menus': list(Menu.objects.values('id', 'name', 'parent_id')),
                        'buttons': available_buttons,
                        'fields': list(MenuField.objects.values('id', 'title', 'menu_id', 'field_name')),
                        'selected_menus': list(RoleMenuPermission.objects.filter(role=role).values_list('menu_id', flat=True)),
                        'selected_buttons': [{'id': x.menu_button_id, 'data_range': x.data_range, 'dept': [dept.pk for dept in x.dept.all()]}
                                             for x in RoleMenuButtonPermission.objects.filter(role=role).prefetch_related('dept')],
                        'selected_fields': list(FieldPermission.objects.filter(role=role).values('field_id', 'is_query', 'is_create', 'is_update')),
                        'departments': list(Dept.objects.values('id', 'name', 'parent_id'))})


class FileViewSet(ResourceViewSet):
    queryset = FileList.objects.select_related('creator').order_by('-pk')
    serializer_class = FileSerializer

    def perform_destroy(self, instance):
        instance.url.delete(save=False)
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return success(msg='附件已删除')

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request):
        for item in self.get_queryset().filter(pk__in=request.data['keys']):
            self.perform_destroy(item)
        return success(msg='附件已删除')


class AreaViewSet(ResourceViewSet):
    queryset = Area.objects.select_related('pcode','creator').order_by('code')
    serializer_class = AreaSerializer

    @action(methods=['get'], detail=False)
    def children(self, request):
        rows = self.filter_queryset(self.get_queryset()).filter(pcode_id=request.query_params.get('pcode')).annotate(children_count=Count('area'))
        return success([{**self.get_serializer(row).data, 'children_count':row.children_count,
                         'has_children':bool(row.children_count)} for row in rows])


class MessageViewSet(ResourceViewSet):
    queryset = MessageCenter.objects.select_related('creator').prefetch_related('target_user', 'target_role', 'target_dept').order_by('-pk')
    serializer_class = serializer_for(MessageCenter)

    def get_queryset(self):
        rows = super().get_queryset()
        return rows.filter(creator=self.request.user) if self.action == 'list' else rows

    def deliver(self, message):
        recipients = {0: lambda: message.target_user.all(),
                      1: lambda: Users.objects.filter(role__in=message.target_role.all()),
                      2: lambda: Users.objects.filter(dept__in=message.target_dept.all()),
                      3: lambda: Users.objects.all()}[message.target_type]().distinct()
        existing = MessageCenterTargetUser.objects.filter(messagecenter=message).values_list('users_id', flat=True)
        pending = list(recipients.exclude(pk__in=existing))
        MessageCenterTargetUser.objects.bulk_create([MessageCenterTargetUser(users=user, messagecenter=message,
            creator=message.creator,modifier=self.request.user,dept_belong=message.dept_belong) for user in pending])
        notify_users([user.pk for user in pending])
        return recipients.count()

    def excel_save(self, serializer, audit, mode):
        message = super().excel_save(serializer, audit, mode)
        if mode == 'create':
            self.deliver(message)
        return message

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        instances = serializer.save(**self.audit())
        for message in instances if isinstance(instances, list) else [instances]:
            self.deliver(message)
        return success(serializer.data, '消息已发送')

    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()
        if MessageCenterTargetUser.objects.filter(users=request.user, messagecenter=message,is_read=False).update(audit_request=request,is_read=True):
            notify_users([request.user.pk])
        return success(self.get_serializer(message).data)

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None):
        message = self.get_object()
        return success({'count': self.deliver(message)}, '消息已发布')

    @action(methods=['get'], detail=True)
    def recipients(self, request, pk=None):
        message=self.get_object()
        rows=MessageCenterTargetUser.objects.filter(messagecenter=message).select_related('users','users__dept').prefetch_related('users__role','users__post').order_by('pk')
        page=self.paginate_queryset(rows)
        return self.get_paginated_response([{'id':row.pk,'is_read':row.is_read,
                                            'user':UserSerializer(row.users,context={'request':request}).data} for row in page])

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def get_self_receive(self, request):
        rows = MessageCenterTargetUser.objects.filter(users=request.user).select_related('messagecenter').order_by('-id')
        page = self.paginate_queryset(rows)
        return self.get_paginated_response([{'id':item.messagecenter_id, 'title':item.messagecenter.title,
            'content':item.messagecenter.content,'is_read':item.is_read,'create_datetime':item.messagecenter.create_datetime} for item in page])

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def get_newest_msg(self, request):
        item = MessageCenterTargetUser.objects.filter(users=request.user).select_related('messagecenter').order_by('-id').first()
        return success({'id':item.messagecenter_id,'title':item.messagecenter.title,'content':item.messagecenter.content,'is_read':item.is_read} if item else None)


class DownloadViewSet(ResourceViewSet):
    queryset = DownloadCenter.objects.select_related('creator').order_by('-pk')
    serializer_class = serializer_for(DownloadCenter)

    def get_queryset(self):
        rows = super().get_queryset()
        return rows if self.request.user.is_superuser else rows.filter(creator=self.request.user)


@extend_schema_view(get=extend_schema(responses=OpenApiTypes.OBJECT),post=extend_schema(request=OpenApiTypes.OBJECT,responses=OpenApiTypes.OBJECT))
class Inbox(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = MessageCenterTargetUser.objects.filter(users=request.user).select_related('messagecenter__creator').order_by('-id')
        unread=messages.filter(is_read=False).count()
        if request.query_params.get('id'):
            get_object_or_404(messages, pk=request.query_params['id'])
            messages = messages.filter(pk=request.query_params['id'])
        if request.query_params.get('search'):
            messages=messages.filter(messagecenter__title__icontains=request.query_params['search'])
        if request.query_params.get('read') in ['true','false']:
            messages=messages.filter(is_read=request.query_params['read']=='true')
        pagination=Pagination()
        page=pagination.paginate_queryset(messages,request)
        return success({'unread': unread,'total':pagination.page.paginator.count,'page':pagination.page.number,
                        'messages': [
            {'id': item.id, 'title': item.messagecenter.title, 'content': item.messagecenter.content,
             'is_read': item.is_read, 'time': serializers.DateTimeField().to_representation(item.messagecenter.create_datetime),
             'sender':str(item.messagecenter.creator) if item.messagecenter.creator else '',
             'receive_time':serializers.DateTimeField().to_representation(item.create_datetime)} for item in page]})

    def post(self, request):
        if MessageCenterTargetUser.objects.filter(users=request.user, pk__in=request.data['ids'],is_read=False).update(audit_request=request,is_read=True):
            notify_users([request.user.pk])
        return success(msg='已标记为已读')


class ConfigViewSet(ResourceViewSet):
    queryset = SystemConfig.objects.order_by('sort', 'pk')
    serializer_class = ConfigSerializer

    @action(methods=['put'], detail=True)
    @transaction.atomic
    def content(self, request, pk=None):
        group = self.get_object()
        children = self.get_queryset().filter(parent=group)
        for child_id in request.data['deleted']:
            get_object_or_404(children, pk=child_id).delete()
        for row in request.data['rows']:
            instance = get_object_or_404(children, pk=row['id']) if row.get('id') else None
            context = {**self.get_serializer_context(),'group':group}
            serializer = self.get_serializer(instance, data=row, partial=instance is not None, context=context)
            serializer.is_valid(raise_exception=True)
            audit = self.audit()
            if instance:
                audit.pop('creator',None)
                audit.pop('dept_belong_id',None)
            serializer.save(parent=group,**audit)
        return success(self.get_serializer(children, many=True).data, msg='分组配置已保存')

    @action(methods=['get'], detail=False)
    def association_tables(self, request):
        return success([{'value':name, 'label':str(model._meta.verbose_name),
                         'pk':model._meta.pk.name,
                         'fields':[{'key':f.name,'title':str(f.verbose_name)} for f in model._meta.fields if model is not Users or f.name not in ['password','groups','user_permissions']]}
                        for name, model in ENTITIES.items()])

    @action(methods=['get'], detail=False)
    def relation_info(self, request):
        key, table = request.query_params['var_name'], request.query_params['table']
        rows = self.get_queryset().filter(key=key, form_item_type__in=[13,14], setting__table=table).select_related('parent')
        model = ENTITIES[table]
        group_ids = set()
        for item in rows:
            field = model._meta.get_field(item.setting.get('primarykey', model._meta.pk.name))
            ids = {field.to_python(value) for value in request.query_params['relation_ids'].split(',')}
            values = item.value if item.form_item_type == 14 else [item.value]
            if values and any(field.to_python(value) in ids for value in values):
                group_ids.add(item.parent_id)
        groups = self.get_queryset().filter(pk__in=group_ids).order_by('sort','pk')
        return success([{'group':self.get_serializer(group).data,
                         'children':self.get_serializer(self.get_queryset().filter(parent=group),many=True).data} for group in groups])

    @action(methods=['get'], detail=True)
    def table_data(self, request, pk=None):
        item = get_object_or_404(self.get_queryset(),pk=pk)
        self.check_object_permissions(request,item)
        entity = item.setting['table']
        view = view_for(entity, ENTITIES[entity])()
        view.request = copy(request)
        view.request._request = copy(request._request)
        view.request._request.path = f'/api/system/{entity}/'
        view.request._request.method = 'GET'
        view.format_kwarg = None
        view.action = 'list'
        view.args = ()
        view.kwargs = {}
        if not ApiPermission().has_permission(view.request,view):
            raise PermissionDenied('无关联数据查询权限')
        search = request.query_params.get('search')
        if search and item.setting.get('searchField'):
            view.request._request.GET = request.query_params.copy()
            del view.request._request.GET['search']
        rows = view.filter_queryset(view.get_queryset())
        if search and item.setting.get('searchField'):
            predicate = Q(pk__in=[])
            allowed = field_access(request.user, ENTITIES[entity])
            for column in item.setting['searchField']:
                key = column['field']
                if column.get('search',True) and key in view.get_serializer().fields and allowed.get(key,{'is_query':True})['is_query']:
                    field = ENTITIES[entity]._meta.get_field(key)
                    predicate |= Q(**{key+('__pk__icontains' if field.is_relation else '__icontains'):search})
            rows = rows.filter(predicate)
        page = self.paginate_queryset(rows)
        data = view.get_serializer(page, many=True).data
        tree_field = item.setting.get('treeField')
        if tree_field:
            model = ENTITIES[entity]
            parent_field = model._meta.get_field(tree_field)
            node_field = parent_field.target_field.name if parent_field.is_relation else model._meta.pk.name
            nodes = [getattr(row,node_field) for row in page]
            parents = set(view.get_queryset().filter(**{tree_field+'__in':nodes}).values_list(tree_field,flat=True))
            for instance, row in zip(page,data):
                row['_tree_id'] = getattr(instance,node_field)
                row['has_children'] = row['_tree_id'] in parents
        return self.get_paginated_response(data)


@extend_schema_view(get=extend_schema(responses=OpenApiTypes.OBJECT))
class DictionaryData(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        key = request.query_params.get('key')
        rows = Dictionary.objects.filter(is_value=True, status=True, parent__status=True)
        if key:
            rows = rows.filter(parent__value=key)
        return success([{'key':row.parent.value, 'label':row.label,
                         'value': dictionary_value(row),
                         'color':row.color} for row in rows.select_related('parent')])


@extend_schema_view(get=extend_schema(responses=OpenApiTypes.OBJECT))
class Metadata(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, entity):
        from plugins.erp_base.source_documents import SourceRecord
        from plugins.erp_base.source_services import literal_default
        if entity not in ENTITIES:
            from django.http import Http404
            raise Http404('此业务资源未启用。')
        model = ENTITIES[entity]
        entry_defaults=set()
        if issubclass(model,SourceRecord):
            from plugins.erp_base.source_entry_registry import ENTRY_RULES
            entry_defaults={model.SOURCE_FIELDS[old] for entry in ENTRY_RULES.get(model._meta.label,{}).values() for old in entry['default_fields']}
        serializer = view_for(entity, model).serializer_class(context={'request': request})
        permissions = field_access(request.user, model)
        fields = []
        model_fields = {field.name: field for field in model._meta.get_fields()}
        for key, field in serializer.fields.items():
            custom = resource_options(model).get('fields', {}).get(key, {})
            if key not in model_fields:
                source = custom.get('source',key).split('.')[0]
                grant = permissions.get(source, {'is_query':True})
                fields.append({'key':key,'title':key,'kind':'text','required':False,'nullable':True,
                               'options':[],'default':None,**custom,'readonly':True,
                               'is_query':grant['is_query'],'is_create':False,'is_update':False})
                continue
            mf = model_fields[key]
            grant = permissions.get(key, {'is_query': True, 'is_create': True, 'is_update': True})
            kind = 'text'
            options = []
            remote = None
            dict_key = dictionary_key(model, key)
            if dict_key:
                kind, options = 'select', dictionary_options(dict_key)
            elif mf.choices:
                kind, options = 'select', [{'label': str(label), 'value': value if isinstance(value, (str,int,float,bool)) else str(value)} for value, label in mf.choices]
            elif mf.is_relation and 'remote' in custom:
                kind = 'multi' if mf.many_to_many else 'select'
                remote = custom['remote']
            elif mf.is_relation:
                kind = 'multi' if mf.many_to_many else 'select'
                related = mf.related_model
                relation_entity = next((name for name, value in ENTITIES.items() if value == related), None)
                if relation_entity:
                    query_request = SimpleNamespace(user=request.user, method='GET', path=f'/api/system/{relation_entity}/')
                    choices = scoped_queryset(related.objects.all(), query_request)
                    if model is Menu and key == 'parent':
                        choices = choices.filter(is_catalog=True)
                    labels = [field.name for field in related._meta.fields if field.name in ['name','title','label','username']]
                    label = labels[0] if labels else related._meta.pk.name
                    remote_models = [Area, Users, Role, Post]
                    options = [{'value':obj.pk, 'label':str(getattr(obj,label)), 'parent':getattr(obj,'parent_id',None)} for obj in choices] if related not in remote_models else []
                    if related in remote_models:
                        remote = {'entity':relation_entity,'pk':related._meta.pk.name,'label':label}
                    if related == Dept:
                        options = [{'value':obj.pk, 'label':obj.name+('（停用）' if not obj.status else ''),
                                    'parent':obj.parent_id,'disabled':not obj.status} for obj in choices]
            elif isinstance(mf, models.BooleanField):
                kind = 'boolean'
            elif isinstance(mf, models.JSONField):
                kind = 'json'
            elif isinstance(mf, models.FileField):
                kind = 'file'
            elif isinstance(mf, models.TextField):
                kind = 'textarea'
            elif isinstance(mf, (models.IntegerField, models.FloatField)):
                kind = 'number'
            elif isinstance(mf, models.DecimalField):
                kind = 'decimal'
            elif isinstance(mf, models.TimeField):
                kind = 'time'
            elif isinstance(mf, models.DateTimeField):
                kind = 'datetime'
            elif isinstance(mf, models.DateField):
                kind = 'date'
            if model is Users and key == 'password':
                kind = 'password'
            if model == MenuField and key == 'model':
                kind = 'select'
                options = [{'value':item._meta.label,'label':f'{item._meta.app_label} · {item._meta.verbose_name} ({item._meta.label})'} for item in permission_models()]
            if model == Menu and key == 'resource':
                kind = 'select'
                options = [{'value':name,'label':f'{item._meta.verbose_name} ({name})'} for name,item in ENTITIES.items()]
            if model == PeriodicTask and key == 'task':
                from application.celery import app
                app.loader.import_default_modules()
                kind = 'select'
                options = [{'label':name,'value':name} for name in app.tasks if not name.startswith('celery.')]
            default = [] if mf.many_to_many else mf.get_default()
            if key in entry_defaults:
                default=None  # 类型、当前日期及登录人等入口默认值留给保存服务，避免被表级常量覆盖。
            elif issubclass(model,SourceRecord) and key in model.SOURCE_DEFAULTS:
                kind_default,value_default=model.SOURCE_DEFAULTS[key]
                if kind_default=='literal':default=literal_default(model,key,value_default)
            if model is Users and key == 'password':
                default = config('base.default_password', 'admin123456')
            if default is not None and not isinstance(default, (str, int, float, bool, list, dict)):
                default = str(default)
            custom = resource_options(model).get('fields', {}).get(key, {})
            fields.append({'key': key, 'title': str(mf.verbose_name), 'kind': kind, 'required': field.required,
                           'readonly': field.read_only, 'nullable': field.allow_null, 'options': options,
                           'default': default, 'remote':remote, 'dictionary':dict_key,
                           'display_key':key+'_label' if mf.is_relation else None,
                           **custom, 'readonly':field.read_only, **grant, **({'is_update':False} if model == Users and key == 'password' else {})})
        if model == Area:
            fields.append({'key':'pcode_name','title':'上级区域名称','kind':'text','options':[],'source':'pcode','required':False,'readonly':True,'default':'','is_query':permissions.get('pcode',{'is_query':True})['is_query'],'is_create':False,'is_update':False})
        if model == Users:
            for source, key, title in [('dept','dept_path','部门路径'),('role','role_names','角色名称'),('post','post_names','岗位名称')]:
                grant = permissions.get(source, {'is_query':True})
                fields.append({'key':key,'title':title,'kind':'text','options':[],'required':False,'readonly':True,
                               'source':source,'default':'','is_query':grant['is_query'],'is_create':False,'is_update':False})
        if 'creator' in model_fields:
            fields.append({'key':'creator_name','title':'创建人姓名','kind':'text','options':[],
                'source':'creator','required':False,'readonly':True,'default':'',
                'is_query':permissions.get('creator',{'is_query':True})['is_query'],'is_create':False,'is_update':False,
                'column':{'show':model == OperationLog and permissions.get('creator',{'is_query':True})['is_query']}})
        from .excel_fields import supports_import
        options = resource_options(model)
        numbering = {}
        if hasattr(model, 'SOURCE_FIELDS'):
            from plugins.erp_base.numbering import policies
            numbering = {'numbering': policies(model)}
        excluded = options.get('exclude_fields', [])
        fields = [field for field in fields if field['key'] not in excluded]
        if 'crud_fields' in options:
            by_key = {field['key']:field for field in fields}
            fields = [by_key[key] for key in options['crud_fields'] if key in by_key]
        return success({'entity': entity, 'title': options.get('title', str(model._meta.verbose_name)), 'pk': model._meta.pk.name,
                        'fields': fields, 'crud_options':options.get('crud_options',{}), 'excel_import': supports_import(model), **numbering,
                        **({'workflow': workflow_actions(entity, view_for(entity, model), options['workflow'])} if 'workflow' in options else {}),
                        **({'resources':[{'entity':name,'title':str(value._meta.verbose_name)} for name,value in ENTITIES.items()]} if model == MenuButton else {})})


SPECIAL_VIEWS = {'user':UserViewSet, 'dept':DeptViewSet, 'menu':MenuViewSet, 'menu_button':MenuButtonViewSet, 'role':RoleViewSet, 'file':FileViewSet, 'area':AreaViewSet, 'dictionary':DictionaryViewSet, 'column':MenuFieldViewSet, 'download_center':DownloadViewSet,
                 'message_center':MessageViewSet, 'system_config':ConfigViewSet, 'periodic_task':PeriodicViewSet}


def view_for(entity, model):
    if entity in SPECIAL_VIEWS:
        return SPECIAL_VIEWS[entity]
    queryset = model.objects.order_by(*(model._meta.ordering or ['-pk']))
    if any(field.name == 'creator' for field in model._meta.fields):
        queryset = queryset.select_related('creator')
    options = resource_options(model)
    view_base = import_string(options['viewset']) if 'viewset' in options else ResourceViewSet
    serializer = serializer_for(model, import_string(options['serializer'])) if 'serializer' in options else serializer_for(model)
    return type(f'{model.__name__}ViewSet', (view_base,), {'queryset': queryset, 'serializer_class': serializer})
