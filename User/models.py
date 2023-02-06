from django.db import models

from tzbapp.settings import MEDIA_ROOT

IDENTITY_CHS = (
    (0, '管理员'),
    (1, '患者'),
    (2, '医生'),
)

SEX_CHS = (
    (0, '未知'),
    (1, '男性'),
    (2, '女性')
)


def upload_to(instance, filename):
    return '/'.join([MEDIA_ROOT, instance.email, filename])


class User(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=50)
    phone = models.CharField(verbose_name='手机号', max_length=50, unique=True, null=True)
    email = models.EmailField(verbose_name='邮箱', max_length=100, unique=True)
    password = models.CharField(verbose_name='密码', max_length=100)
    portrait = models.FileField(verbose_name='头像路径', upload_to=upload_to)
    identity = models.IntegerField(verbose_name='身份', choices=IDENTITY_CHS, default=1)
    sex = models.IntegerField(verbose_name='性别', choices=SEX_CHS, default=0, null=True)
    number = models.CharField(verbose_name='工号', max_length=50, default='')
    patient = models.ManyToManyField('User', related_name='doctor')


class VerifyCode(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=100, verbose_name='用户邮箱', null=True, default='')
    expire_time = models.DateTimeField(verbose_name='过期时间', null=True, default=None)
