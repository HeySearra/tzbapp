import os.path
from django.http import JsonResponse, HttpResponse
import json
import random
import string
import datetime
from django.views import View
from Question.models import Questionare
from User.models import User


class PatientUploadQuestionScore(View):
    def post(self, request):
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 3, 'message': '用户未登录'})
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'time', 'questionare1', 'questionare2', 'questionare3', 'questionare4', 'questionare5'}:
            return JsonResponse({'code': 1, 'message': '参数错误'})
        # 检查参数格式是否正确
        pass
        # 取出request中的参数
        account = kwargs['account']
        time = kwargs['time']
        date_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        questionare1 = kwargs['questionare1']
        # questionare2 = kwargs['questionare2']
        questionare3 = kwargs['questionare3']
        # questionare4 = kwargs['questionare4']
        # questionare5 = kwargs['questionare5']
        user = User.objects.filter(email=account)
        if not user.exists():
            return JsonResponse({'code': 4, 'message': '用户不存在'})
        user= user.get()
        # Questionare.objects.create(user=user, create_time=date_time, score1=questionare1, score2=questionare2,
        #                            score3=questionare3, score4=questionare4, score5=questionare5)
        Questionare.objects.create(user=user, create_time=date_time, score1=questionare1, score3=questionare3)
        return JsonResponse({'code': 0, 'message': '上传成功'})


class DoctorUploadQuestionScore(View):
    def post(self, request):
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 3, 'message': '用户未登录'})
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'time', 'questionare1', 'questionare2', 'questionare3', 'questionare4', 'questionare5'}:
            return JsonResponse({'code': 1, 'message': '参数错误'})
        # 检查参数格式是否正确
        pass
        # 取出request中的参数
        account = kwargs['account']
        time = kwargs['time']
        date_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        # questionare1 = kwargs['questionare1']
        questionare2 = kwargs['questionare2']
        # questionare3 = kwargs['questionare3']
        questionare4 = kwargs['questionare4']
        questionare5 = kwargs['questionare5']
        user = User.objects.filter(email=account)
        if not user.exists():
            return JsonResponse({'code': 4, 'message': '用户不存在'})
        user= user.get()
        # Questionare.objects.create(user=user, create_time=date_time, score1=questionare1, score2=questionare2,
        #                            score3=questionare3, score4=questionare4, score5=questionare5)
        que = Questionare.objects.filter(user=user, create_time=date_time)
        if que.count() != 1:
            return JsonResponse({'code': 6, 'message': '该问卷不存在'})
        que = que.get()
        que.score2 = questionare2
        que.score4 = questionare4
        que.score5 = questionare5
        try:
            que.save()
        except:
            return JsonResponse({'code': 2, 'message': '存储错误'})
        return JsonResponse({'code': 0, 'message': '上传成功'})


class GetQuestionScore(View):
    def post(self, request):
        # 检查登录
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 3, 'message': '用户未登录'})
        kwargs: dict = json.loads(request.body)
        if not {'account'}.issubset(set(kwargs.keys())):
            return JsonResponse({'code': 1, 'message': '参数错误'})
        account = kwargs['account']
        if (account != request.session.get('account', None) and request.session.get('identity', None) == 1):
            return JsonResponse({'code': 7, 'message': '权限错误'})
        user = User.objects.filter(email=account)
        if not user.exists():
            return JsonResponse({'code': 4, 'message': '用户不存在'})
        user = user.get()
        question_list = Questionare.objects.filter(user=user).order_by('-create_time')
        res = {
            'questionScore':[{
                'time': item.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                'score':[
                    item.score1,
                    item.score2,
                    item.score3,
                    item.score4,
                    item.score5
                ]
            }for item in question_list]
        }
        return JsonResponse({'code': 0, 'message': '查询成功', 'questionare': res})


class DeleteQuestion(View):
    def post(self, request):
        # 检查登录
        if not request.session.get('is_login', None) or not request.session['is_login']:
            return JsonResponse({'code': 3, 'message': '用户未登录'})
        kwargs: dict = json.loads(request.body)
        if not {'account', 'time'}.issubset(set(kwargs.keys())):
            return JsonResponse({'code': 1, 'message': '参数错误'})
        account = kwargs['account']
        kwargs_time = kwargs['time']
        if (account != request.session.get('account', None) and request.session.get('identity', None) == 1):
            return JsonResponse({'code': 7, 'message': '权限错误'})
        user = User.objects.filter(email=account)
        if not user.exists():
            return JsonResponse({'code': 4, 'message': '用户不存在'})
