import requests


class YunPian(object):
    """
    云片网发送短信验证码的工具类
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_msg(self, mobile, code):
        parmas = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': f'【周俊峰】您的验证码是{code}。如非本人操作，请忽略本短信'
        }
        rsp = requests.post(self.single_send_url, data=parmas)

