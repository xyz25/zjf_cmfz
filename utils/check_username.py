import django, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zjf_cmfz.settings")
django.setup()
from user.models import User


def check_username(name):
    print([i[0] for i in list(User.objects.values_list('name'))])


if __name__ == '__main__':
    import time

    # t = time.time()
    # t1 = t - 24 * 60 * 60 * 1
    # day1 = time.strftime('%Y-%m-%d', time.gmtime(t1))
    # t2 = t - 24 * 60 * 60 * 2
    # day2 = time.strftime('%Y-%m-%d', time.gmtime(t2))
    # t3 = t - 24 * 60 * 60 * 3
    # day3 = time.strftime('%Y-%m-%d', time.gmtime(t3))
    # t4 = t - 24 * 60 * 60 * 4
    # day4 = time.strftime('%Y-%m-%d', time.gmtime(t4))
    # t5 = t - 24 * 60 * 60 * 5
    # day5 = time.strftime('%Y-%m-%d', time.gmtime(t5))
    # t6 = t - 24 * 60 * 60 * 6
    # day6 = time.strftime('%Y-%m-%d', time.gmtime(t6))
    # t7 = t - 24 * 60 * 60 * 7
    # day7 = time.strftime('%Y-%m-%d', time.gmtime(t7))
    # print(day1, day2, day3, day4, day5, day6, day7)
    # u7 = len(User.objects.filter(register_time=day1))
    # u6 = len(User.objects.filter(register_time=day2))
    # u5 = len(User.objects.filter(register_time=day3))
    # u4 = len(User.objects.filter(register_time=day4))
    # u3 = len(User.objects.filter(register_time=day5))
    # u2 = len(User.objects.filter(register_time=day6))
    # u1 = len(User.objects.filter(register_time=day7))
    # print(u1, u2, u3, u4, u5, u6, u7)
    # data = {
    #     day7: u1,
    #     day6: u2,
    #     day5: u3,
    #     day4: u4,
    #     day3: u5,
    #     day2: u6,
    #     day1: u7
    # }
    #
    provinces = ["北京", "天津", "河北", "山西", "内蒙古", "吉林", "黑龙江", "辽宁", "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北",
                 "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆", "香港", "澳门", "台湾"
                 ]
    data = []
    for i in provinces:
        data.append({'name':i,'value':len(User.objects.filter(address=i))})
        # data[i] = len(User.objects.filter(address=i))
    print(data)
