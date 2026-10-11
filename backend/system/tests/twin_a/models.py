from django.db import models
from core.models import CoreModel

class Twin(CoreModel):
    name=models.CharField('名称',max_length=64)
    only_a=models.CharField('A字段',max_length=64,blank=True)


class BusinessRecord(CoreModel):
    name = models.CharField('业务名称', max_length=64)
    quantity = models.IntegerField('数量', default=0)
    dept_owner = models.CharField('业务负责人', max_length=64, blank=True)
    parent = models.ForeignKey(Twin, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='业务父项')
    tags = models.ManyToManyField(Twin, blank=True, related_name='+', verbose_name='业务标签')

    class Meta:
        abstract = True


class Users(BusinessRecord):
    pass


class LoginLog(BusinessRecord):
    pass


class OperationLog(BusinessRecord):
    pass


class DownloadCenter(BusinessRecord):
    pass


class TaskResult(BusinessRecord):
    pass


class PlainEntry(BusinessRecord):
    pass


class BusinessCredential(CoreModel):
    name = models.CharField('设备名称', max_length=64)
    password = models.CharField('设备口令', max_length=80, default='device-initial')
    groups = models.CharField('业务分组', max_length=64, blank=True)
    user_permissions = models.CharField('业务许可说明', max_length=64, blank=True)


class FileEntry(CoreModel):
    name = models.CharField('资料名称', max_length=64)
    attachment = models.FileField('可选附件', upload_to='fixture/', blank=True)


class ExcludedFileEntry(CoreModel):
    name = models.CharField('资料名称', max_length=64)
    attachment = models.FileField('可选附件', upload_to='fixture/', blank=True)


class RequiredFileEntry(CoreModel):
    name = models.CharField('资料名称', max_length=64)
    attachment = models.FileField('必填附件', upload_to='fixture/')


class BusinessKey(CoreModel):
    id = models.CharField('业务主键', primary_key=True, max_length=64)
    name = models.CharField('名称', max_length=64)
    reference = models.CharField('其他唯一编码', max_length=64, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Twin, blank=True, related_name='+')


class KeyReference(CoreModel):
    target = models.ForeignKey(BusinessKey, on_delete=models.CASCADE)
    alternate = models.ForeignKey(BusinessKey, to_field='reference', on_delete=models.CASCADE, related_name='+')
    targets = models.ManyToManyField(BusinessKey, related_name='+')


class KeyIdentity(models.Model):
    target = models.OneToOneField(BusinessKey, primary_key=True, on_delete=models.CASCADE)


class KeyIdentityReference(models.Model):
    target = models.ForeignKey(KeyIdentity, on_delete=models.CASCADE)
