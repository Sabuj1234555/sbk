from django.shortcuts import render
from django.http import JsonResponse
from .models import QA

def ai(request):
    return render(request, "chat/home.html")

def ask_question(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        question = data.get("question", "")
        try:
            answer = QA.objects.get(question=question).answer
        except QA.DoesNotExist:
            answer = "দুঃখিত, আমি সেটা জানি না।"
        return JsonResponse({"answer": answer})
    return JsonResponse({"answer": "Invalid request"})
