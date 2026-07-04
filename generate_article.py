import json
import os
import requests
from datetime import datetime

HF_TOKEN = os.environ["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

topic = "Latest breakthroughs in artificial intelligence and technology"

def generate_english(prompt):
    # از مدل پایدار distilgpt2 استفاده می‌کنیم (سبک و رایگان)
    model_id = "distilgpt2"
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 600, "temperature": 0.7}
    }
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            # distilgpt2 خروجی را به صورت لیست برمی‌گرداند
            if isinstance(result, list) and len(result) > 0:
                return result[0]["generated_text"].replace(prompt, "").strip()
            else:
                return result.get("generated_text", "").replace(prompt, "").strip()
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return "English content not available at this moment."
    except Exception as e:
        print(f"Request error: {type(e).__name__}: {e}")
        return "English content not available at this moment."

prompt_en = f"Write a detailed article in English about: {topic}. Minimum 4 paragraphs."
article_en = generate_english(prompt_en)
article_fa = article_en   # فعلاً فارسی همان انگلیسی است

# ذخیره در فایل
with open("articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

new_id = len(articles) + 1
today = datetime.now().strftime("%Y/%m/%d")

articles.append({
    "id": new_id,
    "category": "Technology",
    "date": today,
    "title": {"fa": topic, "en": topic},
    "excerpt": {"fa": article_fa[:200] + "...", "en": article_en[:200] + "..."},
    "body": {
        "fa": f"<p>{article_fa.replace(chr(10), '</p><p>')}</p>",
        "en": f"<p>{article_en.replace(chr(10), '</p><p>')}</p>"
    }
})

with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("✅ New article saved.")
