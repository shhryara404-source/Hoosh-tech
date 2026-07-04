import json
import os
from datetime import datetime
from huggingface_hub import InferenceClient

HF_TOKEN = os.environ["HF_TOKEN"]
client = InferenceClient(token=HF_TOKEN)

def generate_article(topic, lang):
    if lang == "fa":
        prompt = f"یک مقاله جامع و تحلیلی به زبان فارسی درباره این موضوع بنویس: {topic}. حداقل ۴ پاراگراف."
    else:
        prompt = f"Write a detailed analysis article in English about: {topic}. Minimum 4 paragraphs."

    response = client.text_generation(
        model="bigscience/bloom-560m",
        prompt=prompt,
        max_new_tokens=800,
        temperature=0.7,
    )
    return response.strip()

topic = "آینده هوش مصنوعی و یادگیری ماشین"
print("Topic:", topic)

article_fa = generate_article(topic, "fa")
article_en = generate_article(topic, "en")

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
    "body": {
        "fa": f"<p>{article_fa.replace(chr(10), '</p><p>')}</p>",
        "en": f"<p>{article_en.replace(chr(10), '</p><p>')}</p>"
    }
}

articles.append(new_article)

with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("✅ مقاله جدید با موفقیت ذخیره شد.")
