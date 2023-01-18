import hashlib
import smtplib
import os
from email.header import Header
from email.mime.text import MIMEText


# MAX
MAX_NAME_LENGTH = 50
MAX_EMAIL_LENGTH = 100
MAX_PASSWORD_LENGTH = 100
MAX_PORTRAIT_LENGTH = 100
# MIN
MIN_NAME_LENGTH = 2
MIN_PASSWORD_LENGTH = 6

# 最大头像尺寸为3MB
MAX_PORTRAIT_SIZE = 3 * 1024 * 1024


# 发送邮件
def send_email(email, verify_code):
    # 邮件服务器
    mail_server = 'smtp.163.com'
    # 发件人邮箱
    mail_sender = 'mlooops@163.com'
    # 发件人邮箱密码
    mail_license = 'EWHBONSUMTFCKYXG'
    # 收件人邮箱
    mail_receivers = email
    # 邮件主题
    mail_subject = 'MLOps注册验证码'
    # 邮件正文
    mail_content = '您的验证码为：' + verify_code
    # 邮件对象
    message = MIMEText(mail_content, 'html', 'utf-8')
    message['From'] = Header(mail_sender, 'utf-8')
    message['To'] = Header(mail_receivers, 'utf-8')
    message['Subject'] = Header(mail_subject, 'utf-8')
    # 发送邮件
    try:
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(host='smtp.163.com')
        server.connect(mail_server, 465)
        # 登录发信邮箱
        server.login(mail_sender, mail_license)
        # 发送邮件
        server.sendmail(mail_sender, mail_receivers, message.as_string())
        # 关闭服务器
        server.quit()
        return True
    except:
        return False

    return True


# 加密密码
def encrypt_password(password):
    # 使用md5加密
    md5 = hashlib.md5()
    salt = "MLops-data".encode('utf-8')
    password = password.encode('utf-8')
    md5.update(password + salt)
    return md5.hexdigest()

# check lambdas
CHECK_SPACE = lambda s: s.count(' ') == 0

CHECK_NAME = lambda name: MAX_NAME_LENGTH >= len(name) >= MIN_NAME_LENGTH

CHECK_EMAIL = lambda email: all([
    len(email) <= MAX_EMAIL_LENGTH,
    CHECK_SPACE(email),
    email.count('@') == 1,
    email.count('.') == 1])

# 密码设置要求不低于6位，不能包含空格，且必须包含数字和字母
CHECK_PASSWORD = lambda password: all([
    len(password) <= MAX_PASSWORD_LENGTH,
    len(password) >= MIN_PASSWORD_LENGTH,
    CHECK_SPACE(password),
    any(char.isdigit() for char in password)
    + any(char.isalpha() for char in password)])
