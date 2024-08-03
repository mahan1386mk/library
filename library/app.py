from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["mynewdb"]
coll = db["users"]

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash("لطفاً هر دو نام کاربری و رمز عبور را وارد کنید.", "danger")
            return redirect(url_for('login'))

        user = coll.find_one({"username": username})
        if user:
            if user["password"] == password:
                flash("ورود موفقیت‌آمیز بود!", "success")
                return redirect(url_for('home'))
            else:
                flash("رمز عبور اشتباه است", "danger")
        else:
            flash("کاربر وجود ندارد. لطفاً ثبت‌نام کنید.", "info")
            return redirect(url_for('register', username=username, password=password))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash("لطفاً هر دو نام کاربری و رمز عبور را وارد کنید.", "danger")
            return redirect(url_for('register'))

        if len(password) <= 4:
            flash("رمز عبور باید بیش از ۴ کاراکتر باشد.", "danger")
            return redirect(url_for('register', username=username, password=password))

        existing_user = coll.find_one({"username": username})
        if existing_user is None:
            coll.insert_one({"username": username, "password": password})
            flash("ثبت‌نام با موفقیت انجام شد!", "success")
            return redirect(url_for('login'))
        else:
            flash("این نام کاربری قبلاً ثبت شده است", "danger")
    
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    
    return render_template('register.html', username=username, password=password)

if __name__ == '__main__':
    app.run(debug=True)
