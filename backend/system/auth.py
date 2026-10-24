from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user_agents import parse
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer, OpenApiTypes
from core.api import success
from .models import Users, LoginLog, SystemConfig
from application.build_version import BUILD_VERSION


def config(key, default=None):
    group, name = key.split('.', 1)
    item = SystemConfig.objects.filter(parent__key=group, key=name).first()
    return item.value if item else default


def public_config(key, default=None):
    group, name = key.split('.', 1)
    item = SystemConfig.objects.filter(parent__key=group, key=name, status=True).first()
    return item.value if item else default


@extend_schema_view(post=extend_schema(request=inline_serializer(name='LoginRequest',fields={
    'username':serializers.CharField(),'password':serializers.CharField(),'captcha':serializers.CharField(required=False),
    'captcha_key':serializers.CharField(required=False)}),responses=OpenApiTypes.OBJECT))
class Login(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data['username']
        agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        log = dict(username=username, ip=request.META.get('REMOTE_ADDR'), browser=agent.browser.family,
                   os=agent.os.family, agent=request.META.get('HTTP_USER_AGENT', ''))
        if config('login.captcha', False):
            challenge = CaptchaStore.objects.filter(hashkey=request.data['captcha_key'], response=request.data['captcha'].lower(), expiration__gt=timezone.now()).first()
            if challenge is None:
                raise serializers.ValidationError('验证码错误')
            challenge.delete()
        account = Users.objects.filter(username=username).first()
        if account is None and username:
            try:
                account = Users.objects.get(Q(email=username) | Q(mobile=username))
            except Users.DoesNotExist:
                account = None
            except Users.MultipleObjectsReturned as exc:
                raise serializers.ValidationError('邮箱或手机号对应多个账号，请使用登录账号') from exc
        user = authenticate(request, username=account.username if account else username, password=request.data['password'])
        if user is None:
            message = '当前用户已被禁用，请联系管理员' if account and not account.is_active and account.check_password(request.data['password']) else '账号或密码错误'
            LoginLog.objects.create(**log, status=False, msg=message)
            raise serializers.ValidationError(message)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        LoginLog.objects.create(**log, status=True, msg='登录成功', creator=user, dept_belong_id=user.dept_id)
        refresh = RefreshToken.for_user(user)
        return success({'access': str(refresh.access_token), 'refresh': str(refresh), 'pwd_change_count': user.pwd_change_count})


@extend_schema_view(get=extend_schema(responses=OpenApiTypes.OBJECT))
class Captcha(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        key = CaptchaStore.generate_key()
        return success({'key': key, 'image': captcha_image_url(key)})


@extend_schema_view(get=extend_schema(responses=OpenApiTypes.OBJECT))
class PublicConfig(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return success({'title': public_config('site.title', 'ERP 管理平台'), 'captcha': config('login.captcha', False),
                        'logo':public_config('site.logo', ''), 'subtitle':public_config('site.subtitle', '组织、权限、系统数据与消息任务'),
                        'copyright':public_config('login.copyright', 'ERP 管理平台'),
                        'keep_record':public_config('login.keep_record', ''), 'help_url':public_config('login.help_url', ''),
                        'privacy_url':public_config('login.privacy_url', '/terms/privacy'), 'clause_url':public_config('login.clause_url', '/terms/service'),
                        'first_password': config('login.first_password', True),
                        'version': BUILD_VERSION})


@extend_schema_view(get=extend_schema(responses=OpenApiTypes.OBJECT))
class PublicConfigValues(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        key = request.query_params.get('key', '')
        prefixes = [prefix for prefix in key.split('|') if prefix]
        rows = SystemConfig.objects.filter(parent__isnull=False, status=True).select_related('parent')
        data = {f'{row.parent.key}.{row.key}':row.value for row in rows}
        return success({name:value for name,value in data.items() if not key or any(name.startswith(prefix) for prefix in prefixes)})


class AuditAPIView(APIView):
    def initial(self, request, *args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            request._request.audit_data = request.data
        return super().initial(request, *args, **kwargs)


@extend_schema_view(get=extend_schema(responses=OpenApiTypes.OBJECT),
    patch=extend_schema(request=OpenApiTypes.OBJECT,responses=OpenApiTypes.OBJECT),
    post=extend_schema(request=inline_serializer(name='UnlockRequest',fields={'password':serializers.CharField()}),responses=OpenApiTypes.OBJECT))
class Account(AuditAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .serializers import AccountSerializer
        from .models import Menu, MenuButton
        user = request.user
        menus = Menu.objects.filter(status=True)
        buttons = MenuButton.objects.all()
        if not user.is_superuser:
            selected = set(menus.filter(rolemenupermission__role__in=user.role.filter(status=True)).values_list('pk', flat=True))
            parents = dict(menus.values_list('id', 'parent_id'))
            # 授权叶页的目录是导航必需项；补祖先不授予同级页或任何接口权限。
            for menu_id in list(selected):
                parent_id = parents[menu_id]
                while parent_id in parents:
                    selected.add(parent_id)
                    parent_id = parents[parent_id]
            menus = menus.filter(pk__in=selected)
            buttons = buttons.filter(rolemenubuttonpermission__role__in=user.role.filter(status=True)).distinct()
        return success({'user': AccountSerializer(user).data,
                        'first_password': config('login.first_password', True),
                        'menus': list(menus.values()), 'buttons': list(buttons.values_list('value', flat=True)),
                        'superuser': user.is_superuser})

    def patch(self, request):
        from .serializers import AccountSerializer
        serializer = AccountSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(modifier=request.user)
        return self.get(request)

    def post(self, request):
        if not request.user.check_password(request.data['password']):
            raise serializers.ValidationError('密码错误')
        return success(msg='解锁成功')


class PasswordRequest(serializers.Serializer):
    new_password = serializers.CharField(trim_whitespace=False)
    new_password_confirm = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm':'两次密码不匹配'})
        return attrs


class PersonalPasswordRequest(PasswordRequest):
    old_password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError({'new_password':'新密码不能与原密码相同'})
        return attrs


@extend_schema_view(post=extend_schema(request=PersonalPasswordRequest,responses=OpenApiTypes.OBJECT))
class Password(AuditAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PersonalPasswordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if not request.user.check_password(data['old_password']):
            raise serializers.ValidationError('原密码错误')
        request.user.set_password(data['new_password'])
        request.user.pwd_change_count += 1
        request.user.save(update_fields=['password', 'pwd_change_count'])
        return success(msg='密码已修改')


@extend_schema_view(post=extend_schema(request=PasswordRequest, responses=OpenApiTypes.OBJECT))
class FirstPassword(AuditAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.pwd_change_count += 1
        request.user.save(update_fields=['password', 'pwd_change_count'])
        return success(msg='首次登录密码已修改')
