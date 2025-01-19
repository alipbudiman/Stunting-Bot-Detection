import json
import re
import requests
from libs.config.config import Config

class Validation(Config):
    def __init__(self) -> None:
        Config().__init__(self)

    def send_whatsapp_otp_verification(self, phone):
        url = f"{self.SERVER_WA_OTP_ADDRESS}/send-otp"
        payload = {
            "phone_number": phone
        }
        
        try:
            response = requests.post(url, json=payload)
            
            body = response.json()
            otp = body.get("otp")
            if otp:
                return otp, None
            else:
                return "", f"Failed to extract OTP from response: {body}"
        
        except requests.exceptions.RequestException as e:
            if self.SERVER_WA_OTP_ADDRESS in str(e):e = str(e).replace(self.SERVER_WA_OTP_ADDRESS, "otp:server:addresses")
            return "", str(e)
    
    def check_whatsapp_otp_verification(self, phone, otp):
        url = f"{self.SERVER_WA_OTP_ADDRESS}/verify-otp"
        payload = {
            "phone_number": phone,
            "otp": otp
        }
        
        try:
            response = requests.post(url, json=payload)
            
            body = response.json()
            success_message = body.get("message")
            if success_message:
                return success_message, None
            else:
                return "", f"OTP verification failed: Data not found, status code: {response.status_code}"
        
        except requests.exceptions.RequestException as e:
            if self.SERVER_WA_OTP_ADDRESS in str(e):e = str(e).replace(self.SERVER_WA_OTP_ADDRESS, "otp:server:addresses")
            return "", str(e)
    

    def CheckPasswordStrength(self, password: str) -> bool:
        # At least 8 characters
        if len(password) < 8:
            return False

        # Contains at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False

        # Contains at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False

        # Contains at least one digit
        if not re.search(r'\d', password):
            return False

        # Contains at least one special character
        if not re.search(r'[!@#$%^&*()_+\-=[\]{};\'":\\|,.<>/?]', password):
            return False

        # Password is strong
        return True
    
    def FormatPhoneNumber(self, phone: str):
        phone = phone.strip()  # Menghilangkan spasi di awal/akhir string

        # Pastikan semua karakter setelah "+" atau sebelum valid
        for i, r in enumerate(phone):
            if i == 0 and r == '+':
                continue
            if not r.isdigit():
                return "", "Nomor telepon hanya boleh berisi angka"

        # Cek prefix nomor telepon
        if phone.startswith("0"):
            # Jika nomor dimulai dengan "0", ganti dengan "+62"
            phone = "62" + phone[1:]
        elif phone.startswith("62"):
            # Jika nomor dimulai dengan "62", tambahkan "+" di depannya
            phone = "62" + phone[2:]
        elif not phone.startswith("62"):
            # Jika nomor tidak sesuai dengan format yang diharapkan
            return "", "Format nomor telepon tidak sesuai"

        return phone, None

    def CheckStringType(self, input_string: str) -> str:
        # Regex untuk memeriksa apakah string adalah email
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        # Regex untuk memeriksa apakah string adalah nomor telepon
        # Memperbolehkan nomor telepon yang dimulai dengan + atau 0
        phone_pattern = r'^(\+?\d{1,3})?0?\d{9,14}$'  # Nomor telepon 10-15 digit, bisa dengan + atau 0 di awal
        
        if re.match(email_pattern, input_string):
            return "email"
        elif re.match(phone_pattern, input_string):
            return "phone"
        else:
            return None


