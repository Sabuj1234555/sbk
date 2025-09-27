import json
import os

# আপনার JSON ডেটা
data = {
  "questions": [
    {
      "id": 1,
      "question": "তোমার নাম কি",
      "answer": "আমার নাম SBK AI চ্যাটবট। আমি আপনার সহায়ক AI।",
      "category": "general"
    },
    {
      "id": 2,
      "question": "html কি",
      "answer": "HTML হলো HyperText Markup Language, যা ওয়েবপেজ তৈরি করতে ব্যবহৃত হয়।",
      "category": "programming"
    },
    {
      "id": 3,
      "question": "পাইথন কি",
      "answer": "পাইথন একটি জনপ্রিয় প্রোগ্রামিং ভাষা যা সহজে শেখা যায় এবং বহুমুখী কাজে ব্যবহার করা যায়।",
      "category": "programming"
    },
    {
      "id": 4,
      "question": "javascript কি",
      "answer": "JavaScript একটি প্রোগ্রামিং ভাষা যা ওয়েবপেজকে ইন্টারেক্টিভ করে তোলে।",
      "category": "programming"
    },
    {
      "id": 5,
      "question": "ধন্যবাদ",
      "answer": "আপনাকেও ধন্যবাদ! আপনার সাথে কথা বলে ভালো লাগল。",
      "category": "general"
    },
    {
      "id": 6,
      "question": "হ্যালো",
      "answer": "হ্যালো! আমি SBK AI চ্যাটবট। আপনার কী সাহায্য লাগবে?",
      "category": "general"
    },
    {
      "id": 7,
      "question": "তুমি কি করতে পারো",
      "answer": "আমি নিম্নলিখিত কাজগুলো করতে পারি:\n• প্রশ্নের উত্তর দিতে পারি\n• JSON ফাইল থেকে ডেটা পড়তে পারি\n• বিভিন্ন প্রোগ্রামিং ভাষায় কোড লিখতে পারি\n• নতুন চ্যাট শুরু করতে পারি\n• প্রশ্ন-উত্তর এডিট করতে পারি",
      "category": "general"
    }
  ]
}

# Django fixture ফরম্যাটে কনভার্ট করুন
fixture_data = []
for i, q in enumerate(data['questions'], 1):
    fixture_data.append({
        "model": "ai.qa",
        "pk": i,
        "fields": {
            "question": q['question'],
            "answer": q['answer'],
            "category": q['category']
        }
    })

# fixtures ডিরেক্টরি তৈরি করুন
os.makedirs('ai/fixtures', exist_ok=True)

# ফাইলে সেভ করুন
with open('ai/fixtures/qa.json', 'w', encoding='utf-8') as f:
    json.dump(fixture_data, f, ensure_ascii=False, indent=2)

print('✅ qa.json ফাইলটি ai/fixtures/ ফোল্ডারে তৈরি করা হয়েছে!')
print('📁 এখন চালান: python manage.py loaddata qa.json')
