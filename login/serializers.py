from rest_framework import serializers
from .models import User

from django.contrib.auth.password_validation import validate_password
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


# read_only: API 출력에는 포함되지만 입력에는 포함되지 않는 필드
# write_only: 인스턴스 생성 시에는 입력에 포함되지만 직렬화에는 포함되지 않게
# required: 역직렬화 중에 제공되지 않으면 오류 발생
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "mobile", "username", "password1", "password2"]
        extra_kwargs = {
            "password1": {
                "write_only": True,
                "required": True,
                "validators": [validate_password],
            },
            "password2": {
                "write_only": True,
                "required": True,
            }
        }

    # 유효성 검사
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    # save() 발생 시
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            mobile=validated_data['mobile'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        token = AuthToken.objects.create(user=user) # 토큰 생성
        return user


# User 모델과 무관하다. 왜냐면 Token 방식으로 인증
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # 사용자가 입력한 ID, PW를 통해 토큰 검사 수행
    def validate(self, data):
        user = authenticate(**data)
        # 가입한 사용자가 맞다면 토큰 반환
        if user:
            token = AuthToken.objects.get(user=user)
            return token
        # 사용자 인증 실패하면 에러 출력
        raise serializers.ValidationError({"error": "로그인 실패"})


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True,)
    new_password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password],)
    new_password2 = serializers.CharField(write_only=True, required=True,)

    def validate(self, data):
        user = get_object_or_404(User, pk=self.request.user)
        # check_password: DB에 저장된 사용자의 비밀번호 AND 사용자가 입력한 비밀번호 비교
        if check_password(data['old_password'], user.password):
            if data['new_password1'] == data['new_password2']:
                return True
            raise serializers.ValidationError({"password": "New_Password fields didn't match."})
        raise serializers.ValidationError({"password": "Old_Password fields didn't match."})

    def create(self, validated_data):
        self.user.set_password(validated_data['new_password1'])
        self.user.save()
        return user


class ChangeUserInfoSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["name", "mobile", "username"]

    def update(self, instance, validated_data):
        # 기존 객체의 정보를 사용자가 입력한 정보로 바꾸거나, 입력하지 않았다면 기존 내용 그대로 유지
        instance.name = validated_data.get('name', instance.name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.username = validated_data.get('username',instance.username)
        return instance

class MypageSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = []
        # 이름, 전화번호, 아이디, 사용자가 작성한 게시글, 사용자가 작성한 댓글






