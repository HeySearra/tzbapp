import os.path

from django.http import JsonResponse
from django.shortcuts import render

import json
import random
import string
import datetime

from django.views import View

from User.models import User, VerifyCode
from User.utils import *


class RegisterView(View):
    def post(self, request):
        print(request.body)
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'account', 'password', 'identity', 'verify_code'}:
            return JsonResponse({'code': 1, 'message': '参数错误'})
        # 检查参数格式是否正确
        pass
        # 取出request中的参数
        name = kwargs['name']
        email = kwargs['account']
        password = encrypt_password(kwargs['password'])
        identity = kwargs['identity']
        verify_code = kwargs['verify_code']
        # 检查邮箱是否已注册
        if User.objects.filter(email=email).exists():
            return JsonResponse({'code': 6, 'message': '邮箱已被注册'})
        # 检查验证码
        vc = VerifyCode.objects.filter(email=email, code=verify_code)
        if not vc.exists():
            return JsonResponse({'code': 7, 'message': '验证码错误或未发送'})
        vc = vc.get()
        # 如果验证码超期
        if vc.expire_time.replace(tzinfo=None) < datetime.datetime.now():
            vc.delete()
            return JsonResponse({'code': 7, 'message': '验证码已过期'})
        # 注册表User
        user = User.objects.create(email=email, password=password, name=name, identity=identity)
        return JsonResponse({'code': 0, 'message': '注册成功', 'uid': user.id})


class LoginView(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'password'}:
            return JsonResponse({'code': 1, 'message': '参数错误'})
        # 取出request中的参数
        email = kwargs['account']
        password = encrypt_password(kwargs['password'])

        user = User.objects.filter(email=email)
        if not user.exists():
            return JsonResponse({'code': 7, 'message': '用户不存在'})
        user = user.get()
        if user.password != password:
            return JsonResponse({'code': 5, 'message': '密码错误'})
        # 在session里保存用户信息
        request.session['is_login'] = True
        request.session['user_id'] = user.id
        request.session['name'] = user.name
        request.session['identity'] = user.identity
        # 设置过期时间为一周
        request.session.set_expiry(60 * 60 * 24 * 7)
        request.session.save()
        return JsonResponse({'code': 0, 'uid': user.id, 'name': user.name ,'message': '登录成功'})


class LogoutView(View):
    def post(self, request):
        if request.session.get('is_login', None):
            request.session['is_login'] = False
        request.session.flush()
        return JsonResponse({'code': 0, 'message': '退出成功'})


class UserInfoView(View):
    def get(self, request):
        # 判断用户是否已登录
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 0, 'message': '用户未登录'})
        user_id = request.session.get('user_id', None)
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return JsonResponse({'code': 0, 'message': '用户不存在'})
        user = user.get()
        return JsonResponse({'code': 1, 'message': '获取成功', 'data': {
            'name': user.name,
            'email': user.email,
            'portrait': user.portrait,
            'identity': user.identity,
        }})


class ChangeUserInfo(View):
    def post(self, request):
        # 判断用户是否已登录
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 0, 'message': '用户未登录'})
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return JsonResponse({'code': 400, 'message': '参数错误'})
        # 取出request中的参数
        name = kwargs['name']

        user_id = request.session.get('user_id', None)
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return JsonResponse({'code': 0, 'message': '用户未注册'})
        user = user.get()
        user.name = name
        user.save()
        return JsonResponse({'code': 1, 'message': '修改成功'})


class SendVerifyCodeView(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'email'}:
            return JsonResponse({'code': 1, 'message': '参数错误'})
        # 取出request中的参数
        email = kwargs['email']
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        # 发送验证码
        if send_email(email, code):
            # 如果数据库中有该email对应的验证码，则删除
            if VerifyCode.objects.filter(email=email).exists():
                VerifyCode.objects.filter(email=email).delete()
            VerifyCode.objects.create(email=email, code=code,
                                      expire_time=datetime.datetime.now() + datetime.timedelta(minutes=5))
            return JsonResponse({'code': 0, 'message': '发送成功'})
        else:
            return JsonResponse({'code': -1, 'message': '发送失败'})


class ChangePassword(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'password', 'verify_code'}:
            return JsonResponse({'code': 400, 'message': '参数错误'})
        # todo:account存在session
        email = kwargs['account']
        password = encrypt_password(kwargs['password'])
        code = kwargs['verify_code']
        # 检查验证码
        vc = VerifyCode.objects.filter(email=email, code=code)
        if not vc.exists():
            return JsonResponse({'code': 0, 'message': '验证码错误或未发送'})
        vc = vc.get()
        # 如果验证码超期
        if vc.expire_time.replace(tzinfo=None) < datetime.datetime.now():
            return JsonResponse({'code': 0, 'message': '验证码已过期'})
        # 修改密码
        user = User.objects.filter(email=email)
        if not user.exists():
            return JsonResponse({'code': 0, 'message': '邮箱未注册'})
        user = user.get()
        user.password = password
        user.save()
        request.session['is_login'] = False
        return JsonResponse({'code': 1, 'message': '修改成功'})


class DeleteUser(View):
    def post(self, request):
        # 判断用户是否已登录
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 0, 'message': '用户未登录'})
        # 如果参数中没有ver
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'verify_code', 'email'}:
            return JsonResponse({'code': 400, 'message': '参数错误'})
        user_id = request.session.get('user_id', None)
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return JsonResponse({'code': 0, 'message': '用户不存在'})
        # 验证验证码是否正确
        email = kwargs['email']
        ver = kwargs['verify_code']
        verify_code = VerifyCode.objects.filter(email=email)
        if not verify_code.exists():
            return JsonResponse({'code': 0, 'message': '未发送验证码'})
        verify_code = verify_code.get()
        if verify_code.code != ver:
            return JsonResponse({'code': 0, 'message': '验证码错误'})
        # 验证码超期
        if verify_code.expire_time.replace(tzinfo=None) < datetime.datetime.now():
            return JsonResponse({'code': 0, 'message': '验证码超期'})
        # 删除用户
        user = user.get()
        user.portrait.delete()
        user.delete()
        # 退出登录
        request.session['is_login'] = False
        return JsonResponse({'code': 1, 'message': '注销成功'})


# 强制删除用户
class DeleteUserForce(View):
    def post(self, request):
        # 判断用户是否已登录
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 0, 'message': '用户未登录'})
        user_id = request.session.get('user_id', None)
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return JsonResponse({'code': 0, 'message': '用户不存在'})
        # 删除用户
        user = user.get()
        email = user.email
        user.portrait.delete()
        user.delete()
        # 退出登录
        request.session['is_login'] = False
        return JsonResponse({'code': 1, 'message': '注销成功，邮箱为' + email})


# 上传图片文件
class UploadPicture(View):
    def post(self, request):
        # 判断用户是否已登录
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 0, 'message': '用户未登录'})
        # 判断是否有文件上传
        if not request.FILES:
            return JsonResponse({'code': 0, 'message': '未上传文件'})
        # 判断文件是否是图片
        file = request.FILES['file']
        if not file.name.split('.')[-1] in ['jpg', 'png', 'jpeg']:
            return JsonResponse({'code': 0, 'message': '文件格式错误'})
        # 判断文件尺寸是否超过限制
        if file.size > MAX_PORTRAIT_SIZE:
            return JsonResponse({'code': 0, 'message': '文件尺寸超过限制'})
        # 保存文件
        user_id = request.session.get('user_id', None)
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return JsonResponse({'code': 0, 'message': '用户不存在'})
        user = user.get()

        user.portrait = file
        user.save()

        return JsonResponse({'code': 1,
                             'message': '上传成功',
                             'file_url': file_url})


class UserInfo(View):
    def post(self, request):
        pass

