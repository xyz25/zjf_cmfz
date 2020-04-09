import django, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zjf_cmfz.settings")
django.setup()
from user.models import User


def check_username(name):
    print([i[0] for i in list(User.objects.values_list('name'))])


if __name__ == '__main__':
    check_username('a')
