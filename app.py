import datetime
import threading
from component import *


from flask import Flask, redirect, request, jsonify, render_template, session
# from flask_cors import CORS
import base64
import time
import uuid
import difflib
from concurrent.futures import ThreadPoolExecutor
from pymongo.mongo_client import MongoClient




app = Flask(__name__)
component = AppComponents()

app.secret_key = component.APP_SECRET


client = MongoClient()
user_db = client.user
account = user_db.account
user_log = user_db.user_log
user_history = user_db.user_history

def clear_history():
    try:
        user_data = user_log.find()
        for data in list(user_data):
            if not data["expired"] or time.time() >= data["expired"]:
                if not data["expired"]:
                    del data["_id"]
                    user_history.insert_one(data)
                user_log.delete_one({"uuid":data["uuid"]})
        
        user_email = account.find()
        for email in list(user_email):
            if email["verify"] == False and email["expired"] <= time.time():
                account.delete_one({"email":email["uuid"]})
    except:pass

def build_data_output(status, input_type, message):
    return {
        "status":status,
        "input":input_type,
        "message":message,    
    }

# Fungsi untuk mengonversi timestamp ke format tanggal yang dapat dibaca (format Indonesia)
def convert_timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y')

# Fungsi untuk mengambil bulan unik dari data dalam format nama bulan
def get_available_months(data):
    months = set()
    for item in data:
        # Ambil nama bulan dalam format nama bulan (misal: Januari, Februari)
        month = datetime.datetime.fromtimestamp(item['timestamp']).strftime('%B')
        months.add(month)
    return sorted(months, key=lambda x: datetime.datetime.strptime(x, '%B').month) 

def bulan_ke_tahun(bulan: int) -> float:
    # 1 tahun = 12 bulan
    tahun = bulan / 12
    return round(tahun, 1)

def is_match(data: str, word: str) -> bool:
    return difflib.SequenceMatcher(None, data.lower(), word.lower()).ratio() >= 0.6

def matchword(text: str, *words: str) -> bool:
    text_words = text.split()

    # Gunakan ThreadPoolExecutor untuk menjalankan perbandingan secara paralel
    with ThreadPoolExecutor() as executor:
        for data in text_words:
            # Jalankan perbandingan untuk setiap data dengan seluruh words
            results = executor.map(lambda w: is_match(data, w), words)
            if any(results):  # Jika ada yang cocok, segera return True
                return True
    return False

def session_clear(session):
    session.clear()

def checkExpiredSessionLogin(session):
    threading.Thread(target=clear_history).start()
    if "email" in session:
        return True
    return False

@app.errorhandler(404)
def page_not_found(e):
    # Render halaman 404 kustom
    return redirect('/')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start():
    return render_template('start.html')

@app.route('/instruction', methods=['GET'])
def instruction():
    if checkExpiredSessionLogin(session):
        return render_template('instruction.html')
    return redirect("/login")
    

@app.route('/logout', methods=['GET'])
def logout():
    session_clear(session)
    return redirect("/login")


@app.route('/login', methods=['GET'])
def login():
    
    if checkExpiredSessionLogin(session):
        return redirect("/start")
    # key = Enc.generate_aes_key()
    # session["SecretKey"] = key
    # key_hex = base64.b64encode(key).decode('utf-8')
    key_hex = ""
    return render_template('login.html', key=key_hex)

@app.route('/login/send', methods=['POST'])
def login_send():    
    email = request.form.get("email", type=str).lower()
    password = request.form.get("password", type=str)
    
    if email == "" or password == "":
        return jsonify({
            'status_code':404,
            'message': 'masukan email / nomor telepon yang valid!',
        }), 404
    
    check_type = component.CheckStringType(email)
    if check_type is None:
        return jsonify({
            'status_code':404,
            'message': 'masukan email / nomor telepon yang valid!',
        }), 404
    elif check_type == "email":
        data = account.find_one({"email":email})
        if data is None or data['verify'] == False:   
            return jsonify({
                'status_code':404,
                'message': 'email tidak terdaftar!',
            }), 404
    else:
        phone, ph_status = component.FormatPhoneNumber(email)
        if ph_status is not None:
            return jsonify({
                'status_code':400,
                'message': ph_status,
                'data':{},
            }), 400
        data = account.find_one({"phone":phone})
        if data is None or data['verify'] == False:   
            return jsonify({
                'status_code':404,
                'message': 'nomor telepon tidak terdaftar!',
            }), 404
            
    if password != data['password']:
        return jsonify({
            'status_code':401,
            'message': 'Password salah!'
        }), 401
        
    # payload = {
    #     'email': email,
    #     'username': data[email]['username'],
    #     'exp': time.time() + Enc.JWT_EXP_DELTA_SECONDS,
    # }
    
    # session["AuthToken"] = Enc.jwt_encode(payload)
    session["email"] = data["email"]

    return jsonify({
        'status_code':200,
        'message': 'Login successful!',
        'data':{
            'forward':"/start"
        }
    }), 200

@app.route('/register', methods=['GET'])
def register():
    # key = Enc.generate_aes_key()
    # session["SecretKey"] = key
    # key_hex = base64.b64encode(key).decode('utf-8')
    key_hex = ""
    return render_template('register.html', key=key_hex)

@app.route('/register/send', methods=['POST'])
def register_send():
    # encrypted_data = request.json.get('data')
    # if not encrypted_data:
    #     return jsonify({'message': 'Encrypted data is missing!'}), 400

    # if 'SecretKey' not in session:
    #     return jsonify({'message': 'SecretKey is missing!'}), 400
    
    # secret_key = session["SecretKey"]
    # decoded_data = Enc.decrypt_data(encrypted_data, secret_key)
    # user_data = eval(decoded_data)
    
    username = request.form.get('username', type=str)
    email = request.form.get('email', type=str).lower()
    phone = request.form.get('phone', type=str)
    password = request.form.get('password', type=str)
    confirm_password = request.form.get('confirm_password', type=str)
    otp = request.form.get('otp', type=str)
    
    if username == "" or email == "" or phone == "" or password == "" or otp == "":
        return jsonify({
            'status_code':400,
            'message': 'data tidak boleh kosong!',
            'data':{},
        }), 400

    if len(username) < 1:
        return jsonify({
            'status_code':400,
            'message': 'username minimal 1 karakter!',
            'data':{},
        }), 400
    
    phone, ph_status = component.FormatPhoneNumber(phone)
    if ph_status is not None:
        return jsonify({
            'status_code':400,
            'message': ph_status,
            'data':{},
        }), 400
        
    check_phone = account.find_one({"phone":phone})
    if check_phone is not None and check_phone["verify"] == True:
        return jsonify({
            'status_code':409,
            'message': 'nomor telepon sudah terdaftar',
            'data':{},
        }), 409
    
    
    if password != confirm_password:
        return jsonify({
            'status_code':400,
            'message': 'konfirmasi password tidak sesuai',
            'data':{},
        }), 400
        
    if not component.CheckPasswordStrength(password):
        return jsonify({
            'status_code':400,
            'message': 'password lemah',
            'data':{},
        }), 400
    
    check_email = account.find_one({"email":email})
    if check_email is not None:
        if check_email["verify"] == True:
            return jsonify({
                'status_code':409,
                'message': 'email sudah terdaftar',
                'data':{},
            }), 409
        elif check_email["verify"] == False and check_email["expired"] <= time.time():
            account.delete_one({"email":email})
        else:
            if otp.isdigit() and len(otp) == 6 and check_email["otp"]["otp_secure"] <= 3:
                if check_email["otp"]["otp_type"] == "wa":success, err = component.check_whatsapp_otp_verification(phone, otp)
                # ganti ke sms
                else:success, err = component.check_whatsapp_otp_verification(phone, otp)
                if err is not None:
                    account.update_one({"email":email},{"$inc":{"otp.otp_secure":1}})
                    return jsonify({
                        'status_code':429,
                        'message': f'otp yang di inputkan salah, percobaan masuk {check_email["otp"]["otp_secure"] + 1} / 3',
                        'data':{},
                    }), 429
                else:
                    account.update_one({"email":email},{
                        "$set":{"verify":True},
                        "$unset":{"otp":None},
                    })
                    session["email"] = email
                    return jsonify({
                        'status_code':200,
                        'message': f'akun anda dengan email {email} sudah terdaftar',
                        'data':{
                            'forward':"/instruction"
                        },
                    }), 200
                        
            else:
                return jsonify({
                    'status_code':429,
                    'message': 'gagal memasukan otp, tunggu selama 10 menit',
                    'data':{},
                }), 429
    else:
        if otp.lower() in ["wa", "sms"]:
            if otp.lower() == "wa":otp_code, err = component.send_whatsapp_otp_verification(phone)
            # ganti ke sms
            else:otp_code, err = component.send_whatsapp_otp_verification(phone)
            if err is not None:
                return jsonify({
                    'status_code':400,
                    'message': err,
                    'data':{},
                }), 400
                
            account.insert_one({
                "email":email,
                "username":username,
                "password":confirm_password,
                "phone":phone,
                "expired":time.time() + 540,
                "otp":{
                    "otp_code":otp_code,
                    "otp_type":otp.lower(),
                    "otp_secure":0,
                    "timestamp":time.time(),
                },
                "verify":False,
            })
            
            return jsonify({
                'status_code':201,
                'message': 'otp send!',
                'data':{
                    'forward':"/instruction"
                },
            }), 200
        else:
            return jsonify({
                'status_code':500,
                'message': 'bad requests!',
                'data':{},
            }), 500
        


@app.route('/input', methods=['GET'])
def input():
    if checkExpiredSessionLogin(session):
        # key = Enc.generate_aes_key()
        # session["SecretKey"] = key
        # key_hex = base64.b64encode(key).decode('utf-8')
        key_hex = ""
        return render_template('input.html', key=key_hex)
    return redirect("/login")

@app.route('/input/send', methods=['POST'])
def input_send():
    if checkExpiredSessionLogin(session):
        # encrypted_data = request.json.get('data')
        # if not encrypted_data:
        #     return jsonify({'message': 'Encrypted data is missing!'}), 400

        # if 'SecretKey' not in session:
        #     return jsonify({'message': 'SecretKey is missing!'}), 400
        
        # secret_key = session["SecretKey"]
        # decoded_data = Enc.decrypt_data(encrypted_data, secret_key)
        # user_data = eval(decoded_data)
        
        nama = request.form.get('nama', type=str)
        umur = request.form.get('umur', type=str)
        bb = request.form.get('bb', type=str)
        tinggi = request.form.get('tinggi', type=str)
        jenis_kelamin = request.form.get('jenis_kelamin', type=str)
        
        if nama == "" or umur == "" or bb == "" or tinggi == "" or jenis_kelamin == "" or int(bb) <= 0 or int(tinggi) <= 0:
            return jsonify({
                'status_code':400,
                'message': 'data tidak boleh kosong!',
                'data':{},
            }), 400
        
        if jenis_kelamin.lower() not in ["l", "p"]:
            return jsonify({
                'status_code':500,
                'message': 'bad request!',
                'data':{},
            }), 500
        
        uuid4 = str(uuid.uuid4())
        
        try:email = session["email"]
        except:
            session_clear(session)
            return jsonify({
                'status_code':500,
                'message': 'not authorize',
                'data':{},
            }), 500
            
        
        user_log.insert_one({
            "email":email,
            "uuid":uuid4,
            "data":{
                "nama":nama,
                "umur":float(umur),
                "bb":float(bb),
                "tinggi":float(tinggi),
                "jenis_kelamin":jenis_kelamin
            },
            "expired":time.time() + 3600,
            "timestamp":time.time(),
        })
        
        return jsonify({
            'status_code':200,
            'message': 'data saved',
            'data':{
                "uuid":uuid4,    
            },
        }), 200
    
    session_clear(session)
    return jsonify({
            'status_code':500,
            'message': 'not authorize',
            'data':{},
        }), 500

@app.route('/dashboard/<uuid>', methods=['GET'])
def dashboard(uuid):
    if checkExpiredSessionLogin(session):
        data_storage = user_log.find_one({"uuid":uuid})
        if data_storage is None:
            return redirect("/input")
        user_data = data_storage["data"]
        if user_data["jenis_kelamin"].lower() == "p":jk = "Perempuan"
        else:jk= "Laki-laki"
        return render_template('dashboard.html', nama=user_data["nama"], umur=round(user_data["umur"]), jenis_kelamin=jk, uuid=uuid )
    return redirect("/login")

@app.route('/chatbot/<uuid>', methods=['GET'])
def chatbot(uuid):
    if checkExpiredSessionLogin(session):
        return render_template('chatbot.html', uuid=uuid)
    
    return redirect("/login")

@app.route('/chatbot/<uuid>/send/<step>', methods=['POST'])
def chatbot_send(uuid, step):
    if checkExpiredSessionLogin(session):
        chat = request.form.get("chat", type=str)
        if chat == "":
            return jsonify({
                'status_code':500,
                'message': 'bad request!',
                'data':{},
            }), 500
        filter_criteria = {"uuid":uuid}
        user_data = user_log.find_one(filter_criteria)
        if user_data is not None:
            if step == "ensure":
                g4_status = matchword(chat, "demam", "muntah", "diare", "iya", "sering sakit", "sering")
                if g4_status:
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output("ask-g4-answer", "6-input", "seberapa yakin anak anda mudah mengalami penyakit infeksi. Contohnya, sering demam, muntah, diare, dan lainnya?"),
                    }), 200
                else:
                    # update g4 before
                    res1, g1, g2 = component.Cfrule1(
                        user_data["data"]["jenis_kelamin"],
                        float(user_data["data"]["umur"]),
                        float(user_data["data"]["tinggi"]),
                        float(user_data["data"]["bb"]),
                        0
                    )
                    
                    new_data = {
                        "list_res":[res1],
                        "cf":{
                            "g1":g1,
                            "g2":g2,
                            "g4":-1,
                        }
                    }
                    user_log.update_one(filter_criteria, {"$set":new_data})
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output(
                            "ask-g3-g5-asking",
                            "chat",
                            "apakah anak anda mengalami kondisi gangguan kemampuan Kognitif atau terlihat lebih gemuk (tinggi tidak bertambah), tumbuh kesamping (gemuk pendek)?"
                        ),
                    }), 200
            
            elif step == "ask-g4-answer":
                g4 = component.TransformUncertainTerm6(chat)
                res1, g1, g2 = component.Cfrule1(
                    user_data["data"]["jenis_kelamin"],
                    float(user_data["data"]["umur"]),
                    float(user_data["data"]["tinggi"]),
                    float(user_data["data"]["bb"]),
                    g4
                )
                new_data = {
                    "list_res":[res1],
                    "cf":{
                        "g1":g1,
                        "g2":g2,
                        "g4":g4,
                    }
                }
                
                user_log.update_one(filter_criteria, {"$set":new_data})
                
                build_msg = component.StuntingSolution(user_data["data"]["umur"], res1)
                
                user_log.update_one(filter_criteria, {"$set":{
                    "expired":False,
                    "confidence_level":res1,
                    "status":"stunting"
                }})
                
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output("stop", "end", build_msg),
                }), 200
            
            elif step == "ask-g3-g5-asking":
                g3g5_status = matchword(chat, "iya", "ada", "terganggu", "lebih gemuk", "terlihat gemuk", "tinggi tidak bertambah", "gemuk pendek", "sepertinya")
                if g3g5_status:
                    msg_build = component.CognitiveImpairmentMessage(user_data["data"]["umur"])
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output("ask-g3-asking", "2-input", msg_build),
                    }), 200
                else:
                    user_log.update_one(filter_criteria, {"$set":{
                        "cf.g3":-1,
                        "cf.g5":-1,
                    }})
                    
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output(
                            "ask-g6-g7-g8-g9-asking",
                            "chat",
                            "Apakah anak anda menjadi lebih pendiam, mengalami Anemia/TBC (dan) penyaki yang selaras, Tidak ASI sampai 6 Bulan dan MPASI dini?",    
                        ),
                    }), 200
            
            elif step == "ask-g3-asking":
                data = component.TransformUncertainTerm2(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g3":data,
                }})
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "ask-g5-asking",
                        "6-input",
                        "apakah anak anda terlihat lebih gemuk (tinggi tidak bertambah), tumbuh kesamping (gemuk pendek)?",
                    ),
                }), 200
            
            elif step == "ask-g5-asking":
                data = component.TransformUncertainTerm6(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g5":data,
                }})
                data_storage = user_log.find_one(filter_criteria)
                user_data = data_storage["cf"]
                res2 = component.Cfrule2(
                    user_data["g2"],
                    user_data["g3"],
                    user_data["g4"],
                    user_data["g5"]
                )
                
                data_storage["list_res"].append(res2)
                max_conf = max(data_storage["list_res"])
                
                update_all = {
                    "$push":{
                        "list_res": res2
                    },
                    "$set":{
                        "expired":False,
                        "confidence_level":max_conf,
                        "status":"stunting"
                    }
                }
                user_log.update_one(filter_criteria, update_all)
                
                build_msg = component.StuntingSolution(data_storage["data"]["umur"], max_conf)
                
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output("stop", "end", build_msg),
                }), 200
            
            elif step == "ask-g6-g7-g8-g9-asking":
                g6g7g8g9status = matchword(chat, "iya", "benar", "mengalami anemia", "mengalami tbc", "mp asi dini", "sering")
                if g6g7g8g9status:
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output(
                            "ask-g6-asking",
                            "6-input",
                            "Apakah anak anda menjadi lebih pendiam (jarang melakukan kontak mata dengan orang di sekitarnya) ?"
                        ),
                    }), 200
                else:
                    user_log.update_one(filter_criteria, {"$set":{
                        "cf.g6":-1,
                        "cf.g7":-1,
                        "cf.g8":-1,
                        "cf.g9":-1,
                    }})
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output(
                            "ask-g3g4-ensure",
                            "chat",
                            "Apakah anak anda terlihat mengalami gangguan kognitif atau terlihat lebih gemuk (tinggi tidak bertambah), tumbuh kesamping (gemuk pendek) ?"
                        ),
                    }), 200

            elif step == "ask-g6-asking":
                data = component.TransformUncertainTerm6(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g6":data,
                }})
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "ask-g7-asking",
                        "6-input",
                        "Apakah anak anda mengalami penyakit Anemia/TBC (dan) penyakit selaras?",
                    ),
                }), 200
            
            elif step == "ask-g7-asking":
                data = component.TransformUncertainTerm6(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g7":data,
                }})
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "ask-g8-asking",
                        "2-input",
                        "Apakah anak anda tidak ASI sampai 6 Bulan?",
                    ),
                }), 200
            
            elif step == "ask-g8-asking":
                data = component.TransformUncertainTerm2(chat)                
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g8":data,
                }})
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "ask-g9-asking",
                        "2-input",
                        "Apakah anak anda MPASI dini?",
                    ),
                }), 200
            
            elif step == "ask-g9-asking":
                data = component.TransformUncertainTerm2(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g9":data,
                }})
                
                data_storage = user_log.find_one(filter_criteria)
                user_data = data_storage["cf"]
                res3 = component.Cfrule3(
                    user_data["g5"],
                    user_data["g6"],
                    user_data["g7"],
                    user_data["g8"],
                    user_data["g9"]
                )
                
                data_storage["list_res"].append(res3)
                max_conf = max(data_storage["list_res"])
                
                update_all = {
                    "$push":{
                        "list_res": res3
                    },
                    "$set":{
                        "expired":False,
                        "confidence_level":max_conf,
                        "status":"stunting"
                    }
                }
                user_log.update_one(filter_criteria, update_all)
                
                build_msg = component.StuntingSolution(data_storage["data"]["umur"], max_conf)
                
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output("stop", "end", build_msg),
                }), 200
            
            elif step == "ask-g3g4-ensure":
                g3g4ensure_status = matchword(chat, "iya", "benar", "mengalami anemia", "mengalami tbc", "mp asi dini", "sering")
                if g3g4ensure_status:
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output(
                            "ask-g3-ensure",
                            "6-input",
                            "Apakah anak anda menjadi lebih pendiam (jarang melakukan kontak mata dengan orang di sekitarnya) ?"
                        ),
                    }), 200
                else: 
                    user_log.update_one(filter_criteria, {"$set":{
                        "cf.g3":0,
                    }})
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output(
                            "ask-g5g6g8g9-ensure",
                            "chat",
                            "Apakah anak anda terlihat lebih gemuk, atau tumbuh kesamping, anak menjadi lebih pendiamn, tidak ASI sampai 6 Bulan dan MPASI dini?"
                        ),
                    }), 200
            
            elif step == "ask-g3-ensure":
                data = component.TransformUncertainTerm6(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g3":data,
                }})
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "ask-g4-ensure",
                        "6-input",
                        "apakah anak anda mudah mengalami penyakit infeksi. Contohnya, sering demam, muntah, diare, dan lainnya?",
                    ),
                }), 200
            
            elif step == "ask-g4-ensure":
                data = component.TransformUncertainTerm6(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g4":data,
                }})
                data_storage = user_log.find_one(filter_criteria)
                user_data = data_storage["cf"]
                res4 = component.Cfrule4(
                    user_data["g3"],
                    user_data["g4"],
                    user_data["g6"],
                    user_data["g8"],
                    user_data["g9"],
                )
                
                data_storage["list_res"].append(res4)
                max_conf = max(data_storage["list_res"])
                
                update_all = {
                    "$push":{
                        "list_res": res4
                    },
                    "$set":{
                        "expired":False,
                        "confidence_level":max_conf,
                        "status":"sakit"
                    }
                }
                user_log.update_one(filter_criteria, update_all)
                            
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "stop",
                        "end",
                        "Anak anda mengalami sakit biasa (normal / tidak stunting)"
                    ),
                }), 200
                

            elif step == "ask-g5g6g8g9-ensure":
                g5g6g8g9ensure_status = matchword(chat, "iya", "benar", "terlihat lebih gemuk", "lebih gemuk", "mp asi dini", "sering", "lebih pendiam")
                if g5g6g8g9ensure_status:
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output(
                            "ask-g5-ensure",
                            "6-input",
                            "Apakah anak nada badan atau bentuk tubuhnya terlihat membesar (gemuk) atau tumbuh kesamping?"
                        ),
                    }), 200
                else:
                    
                    return jsonify({
                        'status_code':200,
                        'message': 'success',
                        'data':build_data_output(
                            "stop",
                            "end",
                            "stunting tidak dapat dideteksi, anak anda kemungkinan tidak mengalami stunting"
                        ),
                    }), 200
            
            elif step == "ask-g5-ensure":
                data = component.TransformUncertainTerm6(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g5":data,
                }})
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "ask-g6-ensure",
                        "6-input",
                        "Dalam kesehariannya, apakah anda melihat bahwa anda ada menjadi lebih pendiam (jarang melakukan kontak mata dengan orang di sekitarnya)?",
                    ),
                }), 200
            
            elif step == "ask-g6-ensure":
                data = component.TransformUncertainTerm6(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g6":data,
                }})
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "ask-g8-ensure",
                        "2-input",
                        "Apakah anak anda tidak mengkonsumsi ASI sampai 6 bulan?",
                    ),
                }), 200
            
            elif step == "ask-g8-ensure":
                data = component.TransformUncertainTerm2(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g8":data,
                }})
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "ask-g9-ensure",
                        "2-input",
                        "Apakah anak anda MPASI dini?",
                    ),
                }), 200
                
            elif step == "ask-g9-ensure":
                data = component.TransformUncertainTerm2(chat)
                user_log.update_one(filter_criteria, {"$set":{
                    "cf.g9":data,
                }})
                
                data_storage = user_log.find_one(filter_criteria)
                user_data = data_storage["cf"]
                res5 = component.Cfrule4(
                    user_data["g3"],
                    user_data["g4"],
                    user_data["g6"],
                    user_data["g8"],
                    user_data["g9"],
                )
                
                data_storage["list_res"].append(res5)
                max_conf = max(data_storage["list_res"])
                
                update_all = {
                    "$push":{
                        "list_res": res5
                    },
                    "$set":{
                        "expired":False,
                        "confidence_level":max_conf,
                        "status":"sakit tinggi"
                    }
                }
                
                user_log.update_one(filter_criteria, update_all)
                            
                return jsonify({
                    'status_code':200,
                    'message': 'success',
                    'data':build_data_output(
                        "stop",
                        "end",
                        "Anak anda mengalami tingkat sakit yang tinggi (sakit tinggi / tidak stunting)"
                    ),
                }), 200    
        
        
        
    session_clear(session)
    return jsonify({
            'status_code':500,
            'message': 'not authorize',
            'data':{},
        }), 500


@app.route('/detail/<uuid>', methods=['GET'])
def detail(uuid):
    if checkExpiredSessionLogin(session):
        return render_template('detail.html', uuid=uuid)
    
    return redirect("/login")

@app.route('/detail/data/<uuid>', methods=['GET'])
def detail_data(uuid):
    if checkExpiredSessionLogin(session):
        data = user_history.find_one({"uuid":uuid})
        if data is not None:
            if data["status"] == "stunting":build_msg = component.StuntingSolution(data["data"]["umur"], data["confidence_level"])
            elif data["status"] == "sakit":build_msg = "Anak anda mengalami sakit biasa (normal / tidak stunting)"
            else:build_msg = "Anak anda mengalami tingkat sakit yang tinggi (sakit tinggi / tidak stunting)"
                
            return jsonify({
                'status_code':200,
                'message': 'success',
                'data':{
                    "level_of_confidence":data["confidence_level"],
                    "message":build_msg,
                },
            }), 200
    
    session_clear(session)
    return jsonify({
            'status_code':500,
            'message': 'not authorize',
            'data':{},
        }), 500

@app.route('/history', methods=['GET'])
def history_load():
    if checkExpiredSessionLogin(session):
        data = user_history.find({"email":session["email"]})
        data = [{"uuid":x["uuid"], "data":x["data"], "timestamp":x["timestamp"], "status": x["status"], "confidence_level":x["confidence_level"] } for x in list(data)]
        available_months = get_available_months(data)
        return render_template('history.html', data=data, available_months=available_months, convert_timestamp_to_date=convert_timestamp_to_date, datetime=datetime, round=round)
    
    return redirect("/login")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=True)