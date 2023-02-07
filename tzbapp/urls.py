"""tzbapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from User.views import *
from Question.view import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/register', RegisterView.as_view()),
    path('account/user_info', UserInfoView.as_view()),
    path('account/login', LoginView.as_view()),
    path('account/logout', LogoutView.as_view()),
    path('account/send_verify_code', SendVerifyCodeView.as_view()),
    path('account/change_user_info', ChangeUserInfo.as_view()),
    path('account/change_password', ChangePassword.as_view()),
    path('account/delete_user', DeleteUser.as_view()),
    path('account/delete_user_force', DeleteUserForce.as_view()),
    path('upload_pic', UploadPicture.as_view()),

    path('doctor/addpatient', AddPatient.as_view()),
    path('doctor/askpatient', GetPatient.as_view()),
    path('doctor/askallpatient', GetAllPatient.as_view()),
    path('doctor/deletequestion', DeleteQuestion.as_view()),
    path('doctor/uploadquestion', DoctorUploadQuestionScore.as_view()),
    path('patient/uploadquestion', PatientUploadQuestionScore.as_view()),
    path('patient/askquestion', GetQuestionScore.as_view()),
    path('patient/askdoctor', GetDoctor.as_view()),
]
