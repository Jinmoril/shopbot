import os
import requests
from moviepy.editor import *

TOPIC = "أسرار النجاح في الإنترنت"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

def generate_script(topic):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"اكتب نص فيديو قصير (30 ثانية) عن: {topic}. اكتب 5 نقاط رئيسية فقط."
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, json=data)
    if r.status_code == 200:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return "النجاح في الإنترنت يتطلب تحديد الأهداف والتعلم المستمر."

def download_images(query, count=5):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": count}
    r = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    images = []
    if r.status_code == 200:
        for i, photo in enumerate(r.json().get("photos", [])[:count]):
            img_data = requests.get(photo["src"]["large"]).content
            path = f"frame_{i}.jpg"
            with open(path, "wb") as f:
                f.write(img_data)
            images.append(path)
    return images

def main():
    print(f"🎬 Creating video about: {TOPIC}")
    script = generate_script(TOPIC)
    print(f"📝 Script: {script[:100]}...")
    print("📥 Downloading images...")
    images = download_images("business success internet", 5)
    print(f"✅ Downloaded {len(images)} images")

if __name__ == "__main__":
    main()