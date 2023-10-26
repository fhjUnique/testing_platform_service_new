# token认证，失效时间 时间单位（秒）
token_expiration_time = 60 * 60 * 24 # 24小时
# token_expiration_time = None

baseAddress = 'https://tool.hujie.online/'

# 文件上传配置  储存到七牛云服务
fsConfig = {
    'fsAddress': 'fs.testing-platform.top',  # 文件服务地址
    'access_key': '4eU_UdLB3wf1jjr6vuC5WWUuIf8Uo3xOcTDsq0o5',  # 需要填写你的 Access Key 和 Secret Key
    'secret_key': 'yLmPCxvOgsH2oLMk16YW2rGvPAe5xY_fOqEwZJBi',
    'bucket_name': 'testing-platform'  # 要上传的空间
}

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testing_platform_test',
        'USER': 'root',
        'PASSWORD': 'Welcome123',
        'HOST': '101.43.173.41',
        'PORT': '3308',
    }
}

# 发送邮件配置
email = {
    'email_server': 'smtp.sina.com',  # 设置服务器
    'email_user': 'fhj_unique@sina.com',
    'email_pass': 'fhj931024',
    'email_receivers': '1136542748@qq.com' # 邮件接收人 商家
}
