import json
import os
import requests
from datetime import datetime

NEWS_API_KEY = os.environ["NEWS_API_KEY"]
HF_TOKEN = os.environ["HF_TOKEN"]

def get_tech_news():
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200:
        articles = resp.json().get("articles", [])
        if articles:
            # انتخاب اولین تیتر خبر
            return articles[0]["title"]
    # اگر خبری پیدا نشد، موضوع پیش‌فرض
    return "پیشرفت‌های جدید در هوش مصنوعی"

def generate_article(topic, lang):
    if lang == "fa":
        prompt = f"یک مقاله جامع و تحلیلی به زبان فارسی درباره این موضوع فناوری بنویس: {topic}. شامل مقدمه، تحلیل، و نتیجه‌گیری باشد. حداقل ۴ پاراگراف."
    else:
        prompt = f"Write a detailed analysis article in English about: {topic}. Include introduction, analysis, and conclusion. At least 4 paragraphs."

    # استفاده از مدل قدرتمند و رایگان
    model_id = "mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {"max_new_tokens": 1200, "temperature": 0.7}
    }

    r = requests.post(f"https://api-inference.huggingface.co/models/{model_id}", headers=headers, json=payload)

    if r.status_code != 200:
        # اگر مدل اول خطا داد، مدل ساده‌تر استفاده شود
        model_id = "bigscience/bloom-560m"
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 800}}
        r = requests.post(f"https://api-inference.huggingface.co/models/{model_id}", headers=headers, json=payload)

    result = r.json()[0]["generated_text"]
    # حذف پرامپت از خروجی
    if lang == "fa":
        result = result.replace(prompt, "").strip()
    else:
        result = result.replace(f"<s>[INST] {prompt} [/INST]", "").strip()
    return result

# ۱. دریافت تیتر خبر روز
topic = get_tech_news()

# ۲. تولید مقاله فارسی و انگلیسی
article_fa = generate_article(topic, "fa")
article_en = generate_article(topic, "en")

# ۳. خواندن فایل articles.json موجود و افزودن مقاله جدید
with open("articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

new_id = len(articles) + 1
today = datetime.now().strftime("%Y/%m/%d")

new_article = {
    "id": new_id,
    "category": "Technology",
    "date": today,
    "title": {"fa": topic, "en": topic},
    "excerpt": {"fa": article_fa[:200] + "...", "en": article_en[:200] + "..."},
    "body": {"fa": f"<p>{article_fa.replace(chr(10), '</p><p>')}</p>",
             "en": f"<p>{article_en.replace(chr(10), '</p><p>')}</p>"}
}

articles.append(new_article)

with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("✅ مقاله جدید با موفقیت تولید و ذخیره شد.")
