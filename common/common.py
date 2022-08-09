from rest_framework.views import APIView


# 앞서 view를 구성할 때 APIView를 상속받아 구현
# 이 과정을 미리 공통 영역에 APIView에서 자신이 추가하고 싶은 내용을 추가 정의한 view 클래스를
# 정의해두고 필요할 때 자신이 정의한 view를 상속받아 사용한다.
# 이 외에도 공통적으로 자주 사용하는 내용을 정의하여 사용할 수 있다.
class ContentView(APIView):
    # 내가 정의한 변수
    user_id = ''
    version = ''

    # APIView에 dispatch 함수를 오버라이딩
    # 자식의 함수가 먼저 호출된 다음 부모 함수를 호출하도록 한다.
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.headers.get('id', False)
        self.version = request.headers.get('version', False)

        return super(ContentView, self).dispatch(request, *args, **kwargs)

