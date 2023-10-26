# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from testing_platform_service.utils.config import email
import logging

logger = logging.getLogger('django')

# 第三方 SMTP 服务
mail_host = email['email_server']  # 设置服务器
mail_user = email['email_user']  # 用户名
mail_pass = email['email_pass']  # 口令

sender = mail_user  # 发送邮件
receivers = email['email_receivers']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱



# subject 发送邮件主题
# mes_value 正文('123', '4', '4', '4', '4')
# receivers 邮件接收人
def send_mail(subject, mes, receivers):
    logger.info('发送邮件>>>')
    message = MIMEMultipart()  # 创建一个带附件的实例
    message['From'] = sender  # 发件人地址
    message['To'] = 'my fans'  # 收件人地址
    message['Subject'] = Header(subject, 'utf-8')
    html_start = '<font face="Courier New, Courier, monospace"><pre>'
    html_end = '</pre></font>'
    # mes = '您有新的订单，请及时处理！<br/>' \
    #       '订单号：   %s<br/>' \
    #       '订单类型： %s<br/>' \
    #       '订单金额： ￥%s<br/>' \
    #       '订单备注： %s<br/>' \
    #       '下单时间： %s<br/>' \
    #       '<br/>'
    # new_mes = mes % mes_value
    message.attach(MIMEText(html_start + mes + html_end, 'html', 'utf-8'))
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        logger.info('发送邮件成功')
    except smtplib.SMTPException as e:
        logger.info(str(e))


# template_create_order = {
#     'subject': '新订单提醒',
#     'mes': '您有新的订单，请及时处理！<br/>' \
#            '订单号：   %s<br/>' \
#            '商品名称： %s<br/>' \
#            '订单类型： %s<br/>' \
#            '订单金额： %s<br/>' \
#            '订单备注： %s<br/>' \
#            '<br/>'
# }
# mes = '您有新的订单，请及时处理！<br/>' \
#           '订单号：   %s<br/>' \
#           '订单类型： %s<br/>' \
#           '订单金额： ￥%s<br/>' \
#           '订单备注： %s<br/>' \
#           '下单时间： %s<br/>' \
#           '<br/>' % ('123', '4', '4', '4', '4')
# send_mail('新订单提醒', mes,'1136542748@qq.com')
