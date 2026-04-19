from django.db import models

class Diary(models.Model):
    original = models.TextField()           # 사용자가 입력한 원문
    ai_version = models.TextField()         # AI가 변환한 일기
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d')} - {self.original[:20]}"