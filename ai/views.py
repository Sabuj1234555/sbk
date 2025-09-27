from django.shortcuts import render
from django.http import JsonResponse
from .models import QA
import json
import requests
from bs4 import BeautifulSoup

def home(request):
    return render(request, "chat/home.html")

def ask(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question", "").lower()

        # Database search
        try:
            qa = QA.objects.filter(question__icontains=question).first()
            if qa:
                return JsonResponse({"answer": qa.answer})
        except:
            pass

        # If not in DB, search online (Google scraping)
        try:
            search_url = f"https://www.google.com/search?q={question}"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            snippet = soup.find("div", class_="BNeawe").get_text()
            return JsonResponse({"answer": snippet})
        except:
            return JsonResponse({"answer": "দুঃখিত, আমি এই প্রশ্নের উত্তর খুঁজে পাইনি।"})

    return JsonResponse({"answer": "Invalid request method. Please send POST request."})

def sync_json_to_db(request):
    # Load qa.json and populate DB
    try:
        with open("qa.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for q in data["questions"]:
            QA.objects.update_or_create(
                question=q["question"],
                defaults={"answer": q["answer"], "category": q.get("category","")}
            )
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)})
import os
import json
from django.http import JsonResponse
from .models import QA

def sync_json_to_db(request):
    # JSON ফাইলের পুরো path
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'qa.json')
    
    if not os.path.exists(path):
        return JsonResponse({"error": f"File not found: {path}"}, status=404)
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for item in data.get('questions', []):
        qa, created = QA.objects.get_or_create(
            question=item['question'],
            defaults={
                'answer': item['answer'],
                'category': item.get('category', 'general')
            }
        )
        if created:
            count += 1

    return JsonResponse({"status": "success", "added": count})