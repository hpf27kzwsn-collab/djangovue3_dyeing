from django.db import models
from core.models import CoreModel

class Twin(CoreModel):
    name=models.CharField('名称',max_length=64)
    only_b=models.CharField('B字段',max_length=64,blank=True)
