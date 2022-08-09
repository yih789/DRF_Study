from rest_framework import serializers
from .models import Content, Comment

# Content의 CRUD를 생각해보자.
# CREATE: title, text, image

### 여기는 모두 ContentSerializer 사용
### 해당 serializer에 content_id 전달하여 retrieve
### 해당 serializer에 3가지 정보만 전달하여 update()
### 해당 serializer 그대로 list
# RETRIEVE: title, text, image, writer_id, created_at, updated_at
# LIST: title, text, image, writer_id, created_at, updated_at
# UPDATE: title, text, image
# DELETE: None

# None pk: CREATE, LIST
# pk: retrieve, update,delete
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content_id', 'text']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content_id', 'commenter_id', 'text', 'created_at', 'updated_at']


class ContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['title', 'text', 'image']


class ContentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    # nested serializer # 게시글에 여러 개의 댓글을 포함한다.
    # Content의 정보를 전달할 때 연결된 comment의 전체 정보까지 함께 준다.

    class Meta:
        model = Content
        fields = ['writer_id', 'title', 'text', 'image', 'comments', 'created_at', 'updated_at']


