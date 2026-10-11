from django.conf import settings
from django.db import models
from django.db import transaction
from collections import Counter
from django.utils import timezone


class CoreQuerySet(models.QuerySet):
    def update(self, request=None, **kwargs):
        if request is not None:
            kwargs.update(modifier=request.user,update_datetime=timezone.now())
        return super().update(**kwargs)


class CoreManager(models.Manager.from_queryset(CoreQuerySet)):
    def create(self, request=None, **kwargs):
        if request is not None:
            kwargs.update(creator=request.user,modifier=request.user,dept_belong_id=request.user.dept_id)
        return super().create(**kwargs)


class CoreModel(models.Model):
    objects = CoreManager()
    description = models.CharField('描述', max_length=255, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建人', null=True,
                                blank=True, on_delete=models.SET_NULL, related_name='+')
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='修改人', null=True,
                                 blank=True, on_delete=models.SET_NULL, related_name='+')
    dept_belong = models.ForeignKey('system.Dept', verbose_name='数据归属部门', null=True,
                                   blank=True, on_delete=models.SET_NULL, related_name='+')
    create_datetime = models.DateTimeField('创建时间', auto_now_add=True)
    update_datetime = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class SoftDeleteQuerySet(CoreQuerySet):
    @transaction.atomic
    def delete(self, soft_delete=True):
        if not soft_delete:
            return super().delete()
        counts=Counter()
        for instance in self:
            _, deleted = instance.delete()
            counts.update(deleted)
        return sum(counts.values()), dict(counts)


class SoftDeleteManager(CoreManager.from_queryset(SoftDeleteQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    @transaction.atomic
    def delete(self, using=None, keep_parents=False, soft_delete=True):
        if not soft_delete:
            return super().delete(using=using,keep_parents=keep_parents)
        counts=Counter({self._meta.label:1})
        for relation in self._meta.related_objects:
            if relation.on_delete == models.CASCADE and issubclass(relation.related_model, SoftDeleteModel):
                _, deleted = relation.related_model.objects.filter(**{relation.field.name:self}).delete()
                counts.update(deleted)
        self.is_deleted = True
        self.save(using=using)
        return sum(counts.values()), dict(counts)
