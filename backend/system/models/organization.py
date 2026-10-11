from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from core.models import CoreModel


class Dept(CoreModel):
    name = models.CharField('部门名称', max_length=64)
    key = models.CharField('部门编码', max_length=64, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='上级部门')
    sort = models.IntegerField('排序', default=1)
    owner = models.CharField('负责人', max_length=64, null=True, blank=True)
    phone = models.CharField('联系电话', max_length=32, null=True, blank=True)
    email = models.EmailField('邮箱', null=True, blank=True)
    status = models.BooleanField('状态', default=True, null=True, blank=True)

    class Meta:
        verbose_name = '部门'
        ordering = ['sort', 'id']
        constraints = [models.UniqueConstraint(fields=['key'], condition=models.Q(key__isnull=False) & ~models.Q(key=''), name='dept_nonempty_key')]

    def __str__(self):
        return self.name


class Role(CoreModel):
    name = models.CharField('角色名称', max_length=64)
    key = models.CharField('权限字符', max_length=64, unique=True)
    sort = models.IntegerField('排序', default=1)
    status = models.BooleanField('状态', default=True)

    class Meta:
        verbose_name = '角色'

    def __str__(self):
        return self.name


class Post(CoreModel):
    name = models.CharField('岗位名称', max_length=64)
    code = models.CharField('岗位编码', max_length=64)
    sort = models.IntegerField('排序', default=1)
    status = models.IntegerField('岗位状态', choices=[(0, '离职'), (1, '在职')], default=1)

    class Meta:
        verbose_name = '岗位'

    def __str__(self):
        return self.name


class Users(CoreModel, AbstractUser):
    objects = UserManager()
    username = models.CharField('用户名', max_length=150, unique=True)
    name = models.CharField('姓名', max_length=64, blank=True)
    mobile = models.CharField('手机号', max_length=255, null=True, blank=True)
    email = models.EmailField('邮箱', max_length=255, null=True, blank=True)
    avatar = models.CharField('头像', max_length=500, null=True, blank=True)
    gender = models.IntegerField('性别', choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, null=True, blank=True)
    dept = models.ForeignKey(Dept, verbose_name='部门', null=True, blank=True, on_delete=models.PROTECT)
    role = models.ManyToManyField(Role, verbose_name='角色', blank=True)
    post = models.ManyToManyField(Post, verbose_name='岗位', blank=True)
    user_type = models.IntegerField('用户类型', choices=[(0, '后台用户'), (1, '前台用户')], default=0, null=True, blank=True)
    pwd_change_count = models.IntegerField('修改密码次数', default=0)

    class Meta:
        verbose_name = '用户'

    def __str__(self):
        return self.name or self.username

    def save(self, *args, **kwargs):
        if self.name == '':
            self.name = self.username
        return super().save(*args, **kwargs)
