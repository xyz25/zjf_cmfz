import random
import string


def get_random_code():
    """
    手机短信随机验证码
    :return:
    """
    return ''.join(random.sample(string.digits, 6))
