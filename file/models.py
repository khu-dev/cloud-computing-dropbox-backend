from django.db import models
from django.conf import settings


# 파일 모델
class File(models.Model):
    file_name = models.CharField(max_length=32, primary_key=True)
    register_date = models.DateTimeField(auto_now_add=True) # 최초 등록일
    modified_date = models.DateTimeField(auto_now=True, null=True) # 수정 날짜
    is_shared = models.BooleanField(default=False)
    file = models.FileField(upload_to='uploaded')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id")  #username이 아닌 user 모델의 id(pk)를 foreignkey로 하여 username 값을 가져오고 싶을 때는 참조하기

    class Meta:
        db_table = "DROPBOX_FILE"