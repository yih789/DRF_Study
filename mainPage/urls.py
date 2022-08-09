from rest_framework.views import APIView
from content.models import Content


class Home(APIView):
    def post(self, request):
        word = request.POST['word']

        contents = Content.objects.filter(title__)
