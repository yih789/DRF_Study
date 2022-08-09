from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from content.serializers import ContentSerializer, ContentCreateSerializer, CommentSerializer, CommentCreateSerializer
from content.models import Content, Comment

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

# 로거 사용
import logging
logger = logging.getLogger('mylogger') # 해당 이름의 로거를 불러온다.


# Content: pk 필요 x
class ContentsAPI(APIView):
    # READ LIST
    def get(self, request):
        contents = Content.objects.all()
        # 여러 개의 contents를 담을 때는 'many=True'를 설정해준다.
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # CREATE
    def post(self, request): # CREATE
        serializer = ContentCreateSerializer(request.FILES)

        if serializer.is_valid():
            serializer.save(writer_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Content: pk 필요
class ContentAPI(APIView):
    # READ RETRIEVE
    def get(self, request, pk):
        content = get_object_or_404(Content, id=pk)
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # UPDATE
    def put(self, request, pk):
        content = get_object_or_404(Content, id=pk)
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        content = get_object_or_404(Content, id=pk)
        result = content.delete() # 삭제
        return Response(result, status=status.HTTP_200_OK)


# Comment: pk 필요 x
class CommentsAPI(APIView):
    # READ RETRIEVE
    def get(self, request):
        comments = Comment.objects.filter(content_id=request.content_id).all()
        serializer = CommentSerializer(comments)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # CREATE
    def post(self, request): # CREATE
        serializer = CommentCreateSerializer(request.data)
        if serializer.is_valid():
            serializer.save(writer_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Comment: pk 필요
class CommentAPI(APIView):
    # UPDATE
    def put(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        # 기존 comment를 수정
        serializer = CommentCreateSerializer(comment, request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        result = comment.delete() # 삭제
        return Response(result, status=status.HTTP_200_OK)


class ContentsPaginationAPI(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['writer_id', 'title', 'text']
    pagination_class =

    def get(self, request): # 모든 content를 pagination으로 제공
        contents = Content.objects.all().order_by('-id')

    def post(self, request): # 사용자가 검색한 특정 키워드의 해당하는 content를 pagination으로 제공
        word = request.POST['word']

        contents = Content.objects.filter(title__icontains=word) | Content.objects.filter(
            text__icontains=word) | Content.objects.filter(writer_id__username__icontains=word)
