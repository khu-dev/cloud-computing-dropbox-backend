from rest_framework.response import Response
from rest_framework.views import APIView

class DummyView(APIView):
    def get(self, request):
        print(request)
        return Response({
            "message": "경희대학교 2021-1 클라우드 컴퓨팅 드롭박스 프로젝트에 오신 것을 환영합니당 ^_^ 연수 배포 성공",
            "confirmed_teammates": ["김연수", "어피치"], ["이재용","삼성"], ["정병기", "테스트"],
        })


