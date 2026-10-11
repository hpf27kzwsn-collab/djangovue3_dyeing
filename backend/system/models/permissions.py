from django.db import models
from core.models import CoreModel
from .organization import Role, Dept


class Menu(CoreModel):
    name = models.CharField('菜单名称', max_length=64)
    parent = models.ForeignKey('self', verbose_name='上级菜单', null=True, blank=True, on_delete=models.CASCADE)
    icon = models.TextField('图标', blank=True)
    sort = models.IntegerField('排序', default=1)
    is_catalog = models.BooleanField('目录', default=False)
    web_path = models.CharField('路由地址', max_length=128, blank=True)
    component = models.CharField('组件地址', max_length=128, blank=True)
    component_name = models.CharField('组件名称', max_length=64, blank=True)
    resource = models.CharField('接口资源', max_length=128, blank=True)
    is_link = models.BooleanField('外链', default=False)
    link_url = models.CharField('链接地址', max_length=500, blank=True)
    is_iframe = models.BooleanField('内嵌页面', default=False)
    status = models.BooleanField('状态', default=True)
    cache = models.BooleanField('页面缓存', default=False)
    visible = models.BooleanField('菜单可见', default=True)
    is_affix = models.BooleanField('固定标签', default=False)

    class Meta:
        verbose_name = '菜单'
        ordering = ['sort', 'id']


class MenuButton(CoreModel):
    menu = models.ForeignKey(Menu, verbose_name='菜单', on_delete=models.CASCADE)
    name = models.CharField('按钮名称', max_length=64)
    value = models.CharField('权限标识', max_length=128, unique=True)
    api = models.CharField('接口地址', max_length=200)
    method = models.IntegerField('请求方法', choices=[(0,'GET'),(1,'POST'),(2,'PUT'),(3,'DELETE'),(4,'OPTIONS'),(5,'PATCH')], default=0)

    class Meta:
        verbose_name = '菜单按钮'


class MenuField(CoreModel):
    menu = models.ForeignKey(Menu, verbose_name='菜单', on_delete=models.CASCADE)
    model = models.CharField('模型', max_length=255)
    field_name = models.CharField('字段', max_length=64)
    title = models.CharField('字段标题', max_length=64)

    class Meta:
        verbose_name = '菜单字段'


class RoleMenuPermission(CoreModel):
    role = models.ForeignKey(Role, verbose_name='角色', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, verbose_name='菜单', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '角色菜单权限'


class RoleMenuButtonPermission(CoreModel):
    role = models.ForeignKey(Role, verbose_name='角色', on_delete=models.CASCADE)
    menu_button = models.ForeignKey(MenuButton, verbose_name='按钮', on_delete=models.CASCADE)
    data_range = models.IntegerField('数据范围', default=0, choices=[(0,'本人'),(1,'本部门及以下'),(2,'本部门'),(3,'全部'),(4,'指定部门')])
    dept = models.ManyToManyField(Dept, verbose_name='指定部门', blank=True)

    class Meta:
        verbose_name = '角色按钮权限'


class FieldPermission(CoreModel):
    role = models.ForeignKey(Role, verbose_name='角色', on_delete=models.CASCADE)
    field = models.ForeignKey(MenuField, verbose_name='字段', on_delete=models.CASCADE)
    is_query = models.BooleanField('可查询', default=True)
    is_create = models.BooleanField('可新增', default=True)
    is_update = models.BooleanField('可修改', default=True)

    class Meta:
        verbose_name = '字段权限'


class ApiWhiteList(CoreModel):
    url = models.CharField('接口地址', max_length=200)
    method = models.IntegerField('请求方法', default=0, choices=MenuButton._meta.get_field('method').choices)
    enable_datasource = models.BooleanField('执行数据权限', default=True)

    class Meta:
        verbose_name = '接口白名单'
