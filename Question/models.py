from django.db import models
from User.models import User


class Questionare(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, to_field="email")
    create_time = models.DateTimeField(null=True)
    score1 = models.FloatField()
    score2 = models.FloatField()
    score3 = models.FloatField()
    score4 = models.FloatField()
    score5 = models.FloatField()


class SWZL(models.Model):
    # 生物治疗反馈仪
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, to_field="email")
    create_time = models.DateTimeField(auto_now_add=True)
    picture = models.CharField(verbose_name='图片', max_length=4096, default='')


class GMZC(models.Model):
    # 肛门直肠测压
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, to_field="email")
    create_time = models.DateTimeField(auto_now_add=True)
    picture = models.CharField(verbose_name='图片', max_length=4096, default='')


# class VedioRecord(models.Model):