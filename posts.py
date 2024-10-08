import os
import json
from flask import Flask, render_template, request, redirect, url_for
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv

load_dotenv()  # Nạp biến môi trường từ tệp .env

# Khởi tạo Firebase
firebase_credentials = json.loads(os.getenv("FIREBASE_CREDENTIALS"))
cred = credentials.Certificate(firebase_credentials)
initialize_app(cred)

db = firestore.client()
app = Flask(__name__)

@app.route('/api/', methods=['GET'])
def index():
    posts = get_posts()  # Lấy danh sách bài đăng từ Firestore
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    app_posts(title, content)  # Thêm bài đăng mới vào Firestore
    return redirect(url_for('index'))

# Lấy danh sách bài đăng từ Firestore
def get_posts():
    posts_ref = db.collection('posts')
    docs = posts_ref.stream()
    posts = [{'title': doc.to_dict()['title'], 'content': doc.to_dict()['content']} for doc in docs]
    return posts

# Thêm bài đăng mới vào Firestore
def app_posts(title, content):
    post = {'title': title, 'content': content}
    db.collection('posts').add(post)

if __name__ == '__main__':
    app.run(debug=True)
