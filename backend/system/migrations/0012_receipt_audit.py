from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [('system', '0011_area_audit')]
    operations = [
        migrations.AddField(model_name='messagecentertargetuser', name='description', field=models.CharField(blank=True,max_length=255,verbose_name='描述')),
        migrations.AddField(model_name='messagecentertargetuser', name='create_datetime', field=models.DateTimeField(auto_now_add=True,default=django.utils.timezone.now,verbose_name='创建时间'),preserve_default=False),
        migrations.AddField(model_name='messagecentertargetuser', name='update_datetime', field=models.DateTimeField(auto_now=True,default=django.utils.timezone.now,verbose_name='修改时间'),preserve_default=False),
        migrations.AddField(model_name='messagecentertargetuser', name='creator', field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='+',to=settings.AUTH_USER_MODEL,verbose_name='创建人')),
        migrations.AddField(model_name='messagecentertargetuser', name='modifier', field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='+',to=settings.AUTH_USER_MODEL,verbose_name='修改人')),
        migrations.AddField(model_name='messagecentertargetuser', name='dept_belong', field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='+',to='system.dept',verbose_name='数据归属部门')),
        migrations.AlterModelOptions(name='messagecentertargetuser',options={'ordering':['-id'],'verbose_name':'消息接收记录'}),
    ]
