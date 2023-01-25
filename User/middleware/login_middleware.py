from django.shortcuts import redirect, render
from django.shortcuts import reverse
from django.utils.deprecation import MiddlewareMixin
from user.models import User


class IsLogin(MiddlewareMixin):     # 中间件检查，未登录且没有写入 list 的 url 头将会被重定向到 login 界面
    # 需要登录
    list = [
        '/captcha', '/register', '/administrator',
        '/resources', '/question',      # for android user, still developing...
        '/test',        # for developer to test new function remember to remove it when start server
        '/android/login', '/login', '/administrator',
        '/admin/', '/administrator',
    ]
    # 不需要登录
    login = [
        '/account', '/administrator',    # 发布时删除最后一项
    ]

    access_check_list = [
        '/admin/', '/administrator',
    ]

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("path:", request.path)
        for s in IsLogin.login:
            if request.path.startswith(s):
                return callback(request, *callback_args, **callback_kwargs)
        # for s in IsLogin.access_check_list:
        #     if request.path.startswith(s) and not request.session.get('permissions', None) in ['admin', 'teacher', 'assistant']:
        #         return redirect(reverse('index'))
        if request.session.get('is_login'):
            try:
                user = User.objects.get(id=request.session.get('user_id'))
            except:
                for s in IsLogin.login:
                    if request.path.startswith(s):
                        return callback(request, *callback_args, **callback_kwargs)
                # for s in IsLogin.access_check_list:
                #     if request.path.startswith(s) and not request.session.get('identity', None) in [0, 2]:
                #         return redirect(reverse('index'))
                user = None
                request.session.flush()
            if user is None or (request.session.session_key != user.session_key and user.session_key != ''):
                request.session.flush()
                return redirect(reverse('login'))
        if request.session.get('is_login', None) is None:
            return redirect(reverse('login'))
        return callback(request, *callback_args, **callback_kwargs)
