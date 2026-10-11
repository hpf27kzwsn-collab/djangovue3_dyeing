from rest_framework import serializers
from core.api import CoreSerializer, AUDIT_FIELDS
from .models import Users, FileList, Dept, Area, Role, Menu, MenuField, SystemConfig, Dictionary
from django.db.models import Max
from rest_framework.validators import UniqueValidator
from .model_catalog import permission_models
from .auth import config
import hashlib
from pypinyin import lazy_pinyin


class AreaSerializer(CoreSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'pcode' in data:
            data['pcode_name'] = instance.pcode.name if instance.pcode else ''
        return data

    class Meta:
        model = Area
        fields = '__all__'
        read_only_fields = AUDIT_FIELDS + ['level', 'pinyin', 'initials']

    def validate(self, attrs):
        name = attrs.get('name', self.instance.name if self.instance else '')
        parent = attrs.get('pcode', self.instance.pcode if self.instance else None)
        pinyin = ''.join(lazy_pinyin(name))
        attrs.update(pinyin=pinyin, initials=pinyin[:1].upper(), level=parent.level+1 if parent else 1)
        return super().validate(attrs)


class AccountSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=255, allow_blank=True, allow_null=True, required=False,
                                   validators=[UniqueValidator(queryset=Users.objects.all(), message='手机号必须唯一')])
    dept_name = serializers.CharField(source='dept.name', read_only=True, default='')
    role_info = serializers.SerializerMethodField()

    def get_role_info(self, instance):
        return list(instance.role.values('id', 'name', 'key'))

    class Meta:
        model = Users
        fields = ['id','username','name','email','mobile','avatar','gender','user_type','dept','dept_name','role','role_info','post','pwd_change_count','last_login']
        read_only_fields = ['id','username','user_type','dept','role','post','pwd_change_count','last_login']


class DictionarySerializer(CoreSerializer):
    class Meta:
        model = Dictionary
        fields = '__all__'
        read_only_fields = AUDIT_FIELDS

    def validate(self, attrs):
        if self.instance is None and attrs.get('parent'):
            attrs['is_value'] = True
        is_value = attrs.get('is_value', self.instance.is_value if self.instance else False)
        kind = attrs.get('type', self.instance.type if self.instance else 0)
        value = attrs.get('value', self.instance.value if self.instance else None)
        if is_value and kind in [1, 6]:
            field = serializers.FloatField() if kind == 1 else serializers.BooleanField()
            try:
                converted = field.run_validation(value)
            except serializers.ValidationError as error:
                raise serializers.ValidationError({'value':error.detail}) from error
            if kind == 6:
                attrs['value'] = str(converted).lower()
        return super().validate(attrs)


class ConfigSerializer(CoreSerializer):
    class Meta:
        model = SystemConfig
        fields = '__all__'
        read_only_fields = AUDIT_FIELDS

    def get_fields(self):
        fields = super().get_fields()
        if 'group' in self.context:
            fields['parent'].default = self.context['group']
        return fields


class OrderedSerializer(CoreSerializer):
    def create(self, validated_data):
        if 'sort' not in validated_data:
            siblings = self.Meta.model.objects.filter(parent=validated_data.get('parent'))
            validated_data['sort'] = (siblings.aggregate(value=Max('sort'))['value'] or 0)+1
        return super().create(validated_data)


class MenuSerializer(OrderedSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = AUDIT_FIELDS


class RoleSerializer(CoreSerializer):
    name = serializers.CharField(max_length=64, validators=[UniqueValidator(queryset=Role.objects.all(), message='角色名称必须唯一')])

    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = AUDIT_FIELDS


class MenuFieldSerializer(CoreSerializer):
    class Meta:
        model = MenuField
        fields = '__all__'
        read_only_fields = AUDIT_FIELDS

    def validate(self, attrs):
        model_name = attrs.get('model', self.instance.model if self.instance else None)
        if model_name not in {model._meta.label for model in permission_models()}:
            raise serializers.ValidationError({'model': '模型不存在或不在字段配置目录'})
        identity = {key:attrs.get(key, getattr(self.instance, key) if self.instance else None)
                    for key in ['menu', 'model', 'field_name']}
        rows = MenuField.objects.filter(**identity)
        if self.instance:
            rows = rows.exclude(pk=self.instance.pk)
        if rows.exists():
            raise serializers.ValidationError({'field_name': '该菜单、模型和字段的权限定义已经存在'})
        return super().validate(attrs)


class DeptSerializer(OrderedSerializer):
    key = serializers.CharField(max_length=64, allow_null=True, allow_blank=True, required=False,
        validators=[UniqueValidator(queryset=Dept.objects.exclude(key=''),message='部门编码必须唯一')])

    class Meta:
        model = Dept
        fields = '__all__'
        read_only_fields = AUDIT_FIELDS

    def create(self, validated_data):
        if 'parent' not in validated_data:
            validated_data['parent'] = self.context['request'].user.dept
        dept = super().create(validated_data)
        dept.dept_belong = dept
        dept.save(update_fields=['dept_belong'])
        return dept


class UserSerializer(CoreSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Users
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff', 'first_name', 'last_name']
        read_only_fields = AUDIT_FIELDS + ['last_login', 'date_joined', 'pwd_change_count']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'dept' in data:
            names, dept = [], instance.dept
            while dept:
                names.insert(0, dept.name)
                dept = dept.parent
            data['dept_path'] = ' / '.join(names)
        for key in ['role', 'post']:
            if key in data:
                data[key+'_names'] = '、'.join(str(obj) for obj in getattr(instance, key).all())
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', config('base.default_password', 'admin123456'))
        roles = validated_data.pop('role', [])
        posts = validated_data.pop('post', [])
        validated_data.pop('dept_belong_id', None)
        validated_data['dept_belong'] = validated_data.get('dept')
        user = Users.objects.create_user(password=password, **validated_data)
        user.role.set(roles)
        user.post.set(posts)
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        validated_data['dept_belong'] = validated_data.get('dept', instance.dept)
        return super().update(instance, validated_data)


class FileSerializer(CoreSerializer):
    class Meta:
        model = FileList
        fields = '__all__'
        read_only_fields = AUDIT_FIELDS + ['size', 'mime_type', 'md5sum', 'file_type']

    def attributes(self, upload):
        digest = hashlib.md5()
        for chunk in upload.chunks():
            digest.update(chunk)
        data = dict(size=upload.size, mime_type=upload.content_type, md5sum=digest.hexdigest(),
                    file_type={'image': 0, 'video': 1, 'audio': 2}.get(upload.content_type.split('/')[0], 3))
        upload.seek(0)
        return data

    def create(self, validated_data):
        upload = validated_data['url']
        validated_data.update(name=upload.name, **self.attributes(upload))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'url' in validated_data:
            validated_data.update(self.attributes(validated_data['url']))
            instance.url.delete(save=False)
        return super().update(instance, validated_data)
