from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from core.models import CoreModel
from .organization import Users, Dept, Role


class Dictionary(CoreModel):
    label = models.CharField('名称', max_length=100, null=True, blank=True)
    value = models.CharField('值', max_length=200, null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name='上级字典', null=True, blank=True, on_delete=models.PROTECT)
    is_value = models.BooleanField('字典项', default=False)
    type = models.IntegerField('类型', choices=[(0,'文本'),(1,'数字'),(2,'日期'),(3,'日期时间'),(4,'时间'),(5,'文件'),(6,'布尔'),(7,'图片')], default=0)
    color = models.CharField('颜色', max_length=32, null=True, blank=True)
    sort = models.IntegerField('排序', default=1, null=True, blank=True)
    status = models.BooleanField('状态', default=True)
    remark = models.CharField('备注', max_length=2000, null=True, blank=True)

    class Meta:
        verbose_name = '字典'
        ordering = ['sort', 'id']
        constraints = [models.UniqueConstraint(fields=['value'], condition=models.Q(parent__isnull=True), name='dictionary_root_value')]


class Area(CoreModel):
    code = models.CharField('区域编码', max_length=20, primary_key=True)
    name = models.CharField('名称', max_length=100)
    pcode = models.ForeignKey('self', verbose_name='上级区域', null=True, blank=True, on_delete=models.CASCADE)
    level = models.IntegerField('层级', default=1)
    pinyin = models.CharField('拼音', max_length=255, blank=True)
    initials = models.CharField('首字母', max_length=20, blank=True)
    enable = models.BooleanField('启用', default=True)

    class Meta:
        verbose_name = '区域'
        ordering = ['code']


class SystemConfig(CoreModel):
    parent = models.ForeignKey('self', verbose_name='分组', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=100)
    key = models.CharField('配置键', max_length=100)
    value = models.JSONField('配置值', default=str, null=True, blank=True)
    sort = models.IntegerField('排序', default=1)
    status = models.BooleanField('前端公开', default=True)
    form_item_type = models.IntegerField('表单类型', default=0, choices=[(0,'文本'),(1,'日期时间'),(2,'日期'),(3,'多行文本'),
        (4,'下拉选择'),(5,'复选框'),(6,'单选框'),(7,'图片'),(8,'文件'),(9,'开关'),(10,'数字'),(11,'数组'),(12,'多图片'),
        (13,'关联对象'),(14,'关联多对象'),(15,'时间')])
    data_options = models.JSONField('选项', default=list, blank=True)
    rule = models.JSONField('规则', default=list, blank=True)
    placeholder = models.CharField('提示', max_length=255, blank=True)
    setting = models.JSONField('设置', default=dict, blank=True)

    class Meta:
        verbose_name = '系统配置'
        ordering = ['sort', 'id']
        constraints = [models.UniqueConstraint(fields=['key', 'parent'], name='config_group_key'),
                       models.UniqueConstraint(fields=['key'], condition=models.Q(parent__isnull=True), name='config_root_key')]


class FileList(CoreModel):
    name = models.CharField('文件名', max_length=255, blank=True)
    url = models.FileField('文件', upload_to='files/%Y/%m')
    size = models.BigIntegerField('大小', default=0)
    mime_type = models.CharField('文件类型', max_length=128, blank=True)
    md5sum = models.CharField('摘要', max_length=32, blank=True)
    upload_method = models.IntegerField('上传方式', choices=[(0, '默认上传'), (1, '文件选择器上传')], default=0)
    file_type = models.IntegerField('文件类别', choices=[(0, '图片'), (1, '视频'), (2, '音频'), (3, '其他')], default=3)

    class Meta:
        verbose_name = '附件'


class OperationLog(CoreModel):
    request_modular = models.CharField('请求模块', max_length=100, blank=True)
    request_msg = models.TextField('操作说明', blank=True)
    json_result = models.JSONField('返回信息', default=dict, encoder=DjangoJSONEncoder)
    request_path = models.CharField('请求路径', max_length=400)
    request_method = models.CharField('请求方法', max_length=16)
    request_body = models.JSONField('请求内容', default=dict)
    response_code = models.IntegerField('响应码', default=2000)
    request_ip = models.GenericIPAddressField('IP', null=True, blank=True)
    request_browser = models.CharField('浏览器', max_length=100, blank=True)
    request_os = models.CharField('操作系统', max_length=100, blank=True)
    status = models.BooleanField('成功', default=True)
    duration = models.FloatField('耗时毫秒', default=0)

    class Meta:
        verbose_name = '操作日志'


class LoginLog(CoreModel):
    login_type = models.IntegerField('登录方式', choices=[(1, '账号密码')], default=1)
    username = models.CharField('账号', max_length=150)
    ip = models.GenericIPAddressField('IP', null=True, blank=True)
    browser = models.CharField('浏览器', max_length=200, blank=True)
    os = models.CharField('操作系统', max_length=200, blank=True)
    status = models.BooleanField('成功', default=True)
    msg = models.CharField('结果', max_length=255, blank=True)
    location = models.CharField('地点', max_length=255, blank=True)
    agent = models.TextField('客户端信息', blank=True)
    continent = models.CharField('洲', max_length=100, blank=True)
    country = models.CharField('国家', max_length=100, blank=True)
    province = models.CharField('省份', max_length=100, blank=True)
    city = models.CharField('城市', max_length=100, blank=True)
    district = models.CharField('区县', max_length=100, blank=True)
    isp = models.CharField('运营商', max_length=100, blank=True)
    area_code = models.CharField('区域编码', max_length=100, blank=True)
    country_english = models.CharField('国家英文名', max_length=100, blank=True)
    country_code = models.CharField('国家代码', max_length=100, blank=True)
    longitude = models.CharField('经度', max_length=100, blank=True)
    latitude = models.CharField('纬度', max_length=100, blank=True)

    class Meta:
        verbose_name = '登录日志'


class MessageCenter(CoreModel):
    target_type = models.IntegerField('消息类型', choices=[(0, '指定用户'), (1, '指定角色'), (2, '指定部门'), (3, '系统通知')], default=0)
    title = models.CharField('标题', max_length=255)
    content = models.TextField('内容')
    target_user = models.ManyToManyField(Users, verbose_name='接收用户', blank=True, related_name='received_messages')
    target_dept = models.ManyToManyField(Dept, verbose_name='接收部门', blank=True)
    target_role = models.ManyToManyField(Role, verbose_name='接收角色', blank=True)

    class Meta:
        verbose_name = '消息'


class MessageCenterTargetUser(CoreModel):
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    messagecenter = models.ForeignKey(MessageCenter, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = '消息接收记录'


class DownloadCenter(CoreModel):
    md5sum = models.CharField('摘要', max_length=32, blank=True)
    task_name = models.CharField('任务名称', max_length=255)
    task_status = models.IntegerField('任务状态', choices=[(0,'已创建'),(1,'运行中'),(2,'完成'),(3,'失败')], default=0)
    file_name = models.CharField('文件名', max_length=255, blank=True)
    url = models.FileField('文件', upload_to='downloads/%Y/%m', blank=True)
    size = models.BigIntegerField('大小', default=0)
    task_id = models.CharField('任务ID', max_length=255, blank=True)

    class Meta:
        verbose_name = '下载任务'
