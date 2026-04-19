import requests
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Diary

def index(request):
    diaries = Diary.objects.order_by('-created_at')
    return render(request, 'diary/index.html', {'diaries': diaries})

def create(request):
    if request.method == 'POST':
        original = request.POST.get('original', '').strip()
        if original:
            ai_version = call_ollama(original)
            Diary.objects.create(original=original, ai_version=ai_version)
        return redirect('index')
    return render(request, 'diary/create.html')

def call_ollama(text):
    prompt = f"""You are a Korean diary writer. You must respond ONLY in Korean language. Never use Chinese or English.

아래 내용을 감성적이고 따뜻한 한국어 일기로 다듬어줘.
반드시 한국어로만 작성해야 해. 중국어나 영어는 절대 사용하지 마.
자연스러운 일기 문체로 3~5문장으로 작성해줘.
일기 내용만 출력하고 다른 설명은 하지 마.

입력: {text}

일기:"""

    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": "gemma3:4b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        return response.json().get('response', '변환 실패')
    except Exception as e:
        return f"오류 발생: {str(e)}"


def delete(request, pk):
    if request.method == 'POST':
        diary = Diary.objects.get(pk=pk)
        diary.delete()
    return redirect('index')