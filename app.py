from flask import Flask, render_template, request, redirect, url_for
from posts import get_posts, app_posts  # Đảm bảo tên đúng

app = Flask(__name__)

@app.route('/api/', methods=['GET'])
def index():
    posts = get_posts()  # Không truyền tham số vào get_posts()
    return render_template('index.html', posts=posts)
    
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    app_posts(title, content)  # Sử dụng đúng hàm app_posts để thêm bài đăng
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)
