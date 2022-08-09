from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=15)  # 기본키
    username = models.CharField(max_length=15, primary_key=True)  # 기본키 # 사용자 ID
    name = models.CharField(max_length=30)  # 사용자 이름

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 복합 기본키
        unique_together = (('username', 'mobile'),)
