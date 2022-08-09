from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from login.models import User
from login.serializers import RegisterSerializer, LoginSerializer, MypageSerializer,ChangePasswordSerializer, ChangeUserInfoSerializer

from django.shortcuts import get_object_or_404


# Register는 post만 수행
class RegisterAPI(APIView):
    def post(self, request):
        # 사용자가 입력한 회원가입 정보를 request로 받아 serializer에 담기
        serializer = RegisterSerializer(data=request.data)
        # 유효성 검사(비밀번호1, 비밀번호2 동일한 지)
        if serializer.is_valid(raise_exception=True):
            serializer.save() # serializer의 save() 요청 => 기본 create() 함수 작동
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Login도 post만 수행
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) # raise_exceiption을 통해 raise된 에러를 전달
        token = serializer.validated_data # validated_data: validate()의 리턴값을 의미, 현재는 Token
        return Response({"token": token.key}, status=status.HTTP_200_OK)


# 회원 비밀번호 수정
class ChangePasswordAPI(APIView):
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        # 유효성 검사
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # serializer의 save() 요청 => 기본 create() 함수 작동
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 권한 필요
class ManageUser(APIView):
    # 마이페이지: 사용자 이름, 전화번호, 사용자가 작성한 글 목록, 사용자가 작성한 댓글 목록
    def get(self, request):
        user = get_object_or_404(User, pk=request.user)
        serializer = MypageSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    # 회원 정보 수정: 이름, 전화번호, 아이디
    def put(self, request):
        user = get_object_or_404(User, pk=request.user)
        # 기존 User 정보를 가져오고, 사용자가 새롭게 요청한 데이터를 넣어 저장한다.
        serializer = ChangeUserInfoSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save() # 이미 존재하는 객체는 update(), 객체가 없다면 create()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 탈퇴
    def delete(self, request):
        user = get_object_or_404(User, pk=request.user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








