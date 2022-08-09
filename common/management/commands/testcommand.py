from django.core.management import BaseCommand

# 이름 무조건 Command!
class Command(BaseCommand):
    def handle(self, *args, **option):
        for i in range(10):
            print('텍스트 배치 실행', i)