from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
import random
import string

app = Flask(__name__)

# ข้อมูลคำถามและคำตอบของแชทบอท
chatbot_data = [
    {
        "tag": "greeting",
        "patterns": ["สวัสดี", "หวัดดี", "สวัสดีครับ", "สวัสดีค่ะ", "ดีจ้า", "สวัสดีตอนเช้า"],
        "responses": ["สวัสดีครับ มีอะไรให้ช่วยไหม?", "สวัสดีครับคุณ!", "ยินดีต้อนรับครับ!"]
    },
    {
        "tag": "sell",
        "patterns": ["ขายอะไรบ้าง", "มีสินค้าอะไร", "มีอะไรขาย", "มีอะไรให้แนะนำ" , "ขายไร"],
        "responses": ["เรามีชากับกาแฟครับ", "สินค้าของเรามีชากับกัญชา"]
    },
    {
        "tag": "age",
        "patterns": ["คุณอายุเท่าไหร่", "แชทบอทอายุเท่าไหร่", "คุณเกิดเมื่อไหร่"],
        "responses": ["ผมอายุ 18 ปีครับ", "ผมยังเด็กอยู่ครับ แค่ 18 ปี"]
    }
]

# ฟังก์ชันการประมวลผลข้อความเข้า
def preprocess_text(text):
    # แปลงเป็นตัวพิมพ์เล็กและลบเครื่องหมายวรรคตอน
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# ฟังก์ชันค้นหาคำถามที่ใกล้เคียงที่สุดโดยใช้ fuzzywuzzy
def get_closest_response(user_input):
    user_input = preprocess_text(user_input)
    patterns = []
    tag_map = {}

    for intent in chatbot_data:
        for pattern in intent['patterns']:
            pattern = preprocess_text(pattern)
            patterns.append(pattern)
            tag_map[pattern] = intent['responses']

    # ใช้ fuzzywuzzy เพื่อค้นหาข้อความที่ใกล้เคียงที่สุด
    closest_match, similarity_score = process.extractOne(user_input, patterns)

    THRESHOLD = 70  # กำหนดค่าความคล้ายคลึงขั้นต่ำ
    if similarity_score < THRESHOLD:
        return "ขอโทษครับ ผมไม่เข้าใจสิ่งที่คุณสื่อสาร"

    # เลือกคำตอบจากแพทเทิร์นที่ใกล้เคียงที่สุด
    return random.choice(tag_map[closest_match])

# Route สำหรับแสดงหน้าเว็บหลัก
@app.route('/')
def index():
    return render_template('index.html')

# Route สำหรับรับคำถามจากผู้ใช้และตอบกลับ
@app.route('/get-response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')
    bot_response = get_closest_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
