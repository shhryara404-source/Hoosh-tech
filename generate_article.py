import json
import os
from datetime import datetime
from huggingface_hub import InferenceClient

HF_TOKEN = os.environ["HF_TOKEN"]
client = InferenceClient(token=HF_TOKEN)

topic = "Latest breakthroughs in artificial intelligence and technology"

def generate_english(prompt):
    try:
        response = client.text_generation(
            model="gpt2",
            prompt=prompt,
            max_new_tokens=600,
            temperature=0.7,
        )
        return response.strip()
    except Exception as e:
        print(f"English error: {type(e).__name__}: {e}")
        return "English content not available at this moment."

prompt_en = f"Write a detailed article in English about: {topic}. Minimum 4 paragraphs."
article_en = generate_english(prompt_en)
# فعلاً فارسی همان انگلیسی است (بعداً ترجمه می‌کنیم)
article_fa = article_en

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
