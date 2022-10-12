
import smtplib
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
 
sender = 'ziruwang113@gmail.com'
receivers = ['ziruwang113@gmail.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')   # 发送者
message['To'] =  Header("测试", 'utf-8')        # 接收者
 
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
 
 
user = 'ziruwang113@gmail.com'
password = 'w8835962'
 
smtpserver = 'smtp.gmail.com'

while(1)
smtp = smtplib.SMTP_SSL(smtpserver,465)
smtp.login(user,password)
smtp.sendmail(sender, receivers, message.as_string())
