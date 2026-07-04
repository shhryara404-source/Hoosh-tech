import json
import os
from datetime import datetime
from huggingface_hub import InferenceClient

HF_TOKEN = os.environ["HF_TOKEN"]
client = InferenceClient(token=HF_TOKEN)

topic = "پیشرفت‌های جدید در هوش مصنوعی و فناوری"

def generate_article(prompt):
    try:
        response = client.text_generation(
            model="distilgpt2",
            prompt=prompt,
            max_new_tokens=800,
            temperature=0.7,
        )
        return response.strip()
    except Exception as e:
        print(f"خطا در تولید متن: {type(e).__name__}: {e}")
        # اگر پاسخ خطا شامل جزئیات بیشتری است، آن را هم چاپ کن
        if hasattr(e, 'response'):
            print("Response text:", e.response.text)
        return "محتوای مقاله در این لحظه در دسترس نیست."

prompt_fa = f"یک مقاله جامع به زبان فارسی درباره این موضوع بنویس: {topic}. حداقل ۴ پاراگراف."
prompt_en = f"Write a detailed article in English about: {topic}. Minimum 4 paragraphs."

article_fa = generate_article(prompt_fa)
article_en = generate_article(prompt_en)

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

print("✅ مقاله جدید ذخیره شد.")
