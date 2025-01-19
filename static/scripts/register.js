function validateEmail(email) {
    // Regex untuk memvalidasi format email
    const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    
    return emailPattern.test(email);
}

function formatPhoneNumber(phone) {
    // Menghilangkan spasi di awal/akhir string
    phone = phone.trim();

    // Validasi apakah hanya terdiri dari angka (kecuali '+' di awal)
    const phoneRegex = /^\+?[0-9]*$/;
    if (!phoneRegex.test(phone)) {
        return "Nomor telepon hanya boleh berisi angka"
    }

    if (phone.startsWith("0")) {
        // Jika nomor dimulai dengan "0", ganti dengan "+62"
        phone = "+62" + phone.substring(1);
        return ""
    } else if (phone.startsWith("62")) {
        // Jika nomor dimulai dengan "62", tambahkan "+" di depannya
        phone = "+62" + phone.substring(2);
        return ""
    } else if (!phone.startsWith("+62")) {
        return "Format nomor telepon tidak sesuai, contoh: 08122357711"
    }

    return "";
}

function StatusMessageDaftar(action, message, location) {
    const status_message = document.getElementById(`daftar-status message-${location}`)
    if (status_message) {
        if (action == "green") {
            status_message.style.color = 'green'
            status_message.textContent = message;
            status_message.style.visibility = 'visible';
            status_message.style.color = 'green'
            status_message.style.position = 'relative';
        }
        if (action == true) {
            status_message.style.color = 'black'
            status_message.textContent = message;
            status_message.style.visibility = 'visible';
            status_message.style.position = 'relative';
        } else if (action == false) {
            status_message.textContent = 'empty';
            status_message.style.visibility = 'hidden';
            status_message.style.position = 'absolute';
        }
    }
}

function checkStrongUsernamePassword(password, username) {
    var panjangMinimal = 1;
    var memilikiHurufKapital = /[A-Z]/.test(password);
    var memilikiHurufKecil = /[a-z]/.test(password);
    var memilikiAngka = /\d/.test(password);
    var memilikiKarakterKhusus = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (username != 0) {
        if (username.length < panjangMinimal) {
            return 'Username harus minimal ' + panjangMinimal + ' karakter';
        } else {
            return 200
        }   
    }

    if (password != 0) {
        if (!memilikiHurufKapital) {
            return 'Kata sandi harus mengandung setidaknya satu huruf kapital';
        } else if (!memilikiHurufKecil) {
            return 'Kata sandi harus mengandung setidaknya satu huruf kecil';
        } else if (!memilikiAngka) {
            return 'Kata sandi harus mengandung setidaknya satu angka';
        } else if (!memilikiKarakterKhusus) {
            return 'Kata sandi harus mengandung setidaknya satu karakter khusus';
        } if (password.length < panjangMinimal) {
            return 'Kata sandi harus minimal ' + panjangMinimal + ' karakter';
        } else {
            return 200;
        }
    }
}


function SendRegister(){
    return new Promise((resolve, riject)=>{
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const phone = document.getElementById("phone").value;
        const password = document.getElementById("password").value;
        const confirm_password = document.getElementById("confirm_password").value;
        let otp = document.getElementById("otp").value;
        if (otp == "") {otp = document.getElementById("otp-type").value}
        console.log(otp)
        $.ajax({
            type: "POST",
            url: "/register/send",
            data: {
                username: username,
                email: email,
                phone:phone,
                password: password,
                confirm_password: confirm_password,
                otp:otp,
            },
            success: (response) => {
                resolve(response)
            },
            error: (xhr, status, error) => {
                const err = JSON.parse(xhr.responseText)
                try {
                    riject(`[Error: ${err.status_code}] ${err.message}`)
                } catch (er) {
                    riject(`[Error: ${status}] ${error}`)
                }
            }
        });
    })

}

const hide = document.getElementById("hide-password")
hide.addEventListener('click', ()=> {
    const password = document.getElementById("password");
    const confirm_password = document.getElementById("confirm_password");
    if (hide.textContent.toLowerCase() === 'jangan sembunyikan password') {
        password.type = 'text';
        confirm_password.type = 'text';
        hide.textContent = 'sembunyikan password'

    } else {
        password.type = 'password';
        confirm_password.type = 'password';
        hide.textContent = 'jangan sembunyikan password'
    }

})

const username_btn = document.getElementById('username');
username_btn.addEventListener('keyup', () => {
    if (username_btn.value == "") {
        StatusMessageDaftar(false, "", 'username');
        return
    }
    const is_strong = checkStrongUsernamePassword(0, username_btn.value);
    if (is_strong != 200) {
        StatusMessageDaftar(true, is_strong, 'username');
    } else {
        StatusMessageDaftar(false, "", 'username');
    }
})

const email_btn = document.getElementById('email');
email_btn.addEventListener('keyup', () => {
    if (email_btn.value == "") {
        StatusMessageDaftar(false, "", 'email');
        return
    }
    const status = validateEmail(email_btn.value);
    if (!status) {
        StatusMessageDaftar(true, "email tidak valid", 'email');
    } else {
        StatusMessageDaftar(false, "", 'email');
    }
})

const phone_btn = document.getElementById('phone');
phone_btn.addEventListener('keyup', () => {
    if (phone_btn.value == "") {
        StatusMessageDaftar(false, "", 'phone');
        return
    }
    const status = formatPhoneNumber(phone_btn.value);
    if (status != "") {
        StatusMessageDaftar(true, message, 'phone');
    } else {
        StatusMessageDaftar(false,"", 'phone');
    }
})

const password_btn = document.getElementById('password');
password_btn.addEventListener('keyup', ()=> {
    if (password_btn.value == "") {
        StatusMessageDaftar(false, "", 'password');
        return
    }
    const is_strong = checkStrongUsernamePassword(password_btn.value, 0);
    if (is_strong != 200) {
        StatusMessageDaftar(true, is_strong, 'password');
    } else if (password_btn.value != "" && password_btn.value != password_btn.value) {
        StatusMessageDaftar(true, "password tidak cocok, harap periksa kembali!", 'password');
    } else {
        StatusMessageDaftar(false, "", 'password')
    }
})

const confirm_password_btn = document.getElementById('confirm_password');
confirm_password_btn.addEventListener('keyup', ()=> {
    if (confirm_password_btn.value == "") {
        StatusMessageDaftar(false, "", 'confirm_password');
        return
    }
    if (password_btn.value === "") {
        StatusMessageDaftar(true, "Harap masukan password terlebih dahulu!", 'confirm_password');
    } else if (password_btn.value != confirm_password_btn.value) {
        StatusMessageDaftar(true, "password tidak cocok, harap periksa kembali!", 'confirm_password');
    } else {
        StatusMessageDaftar(false, "", 'confirm_password');
    }
})

const regbtn = document.getElementById("regsiterbtn");
regbtn.addEventListener('click', () => {
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const phone = document.getElementById("phone");
    const password = document.getElementById("password");
    const confirm_password = document.getElementById("confirm_password");
    const otp = document.getElementById("otp");
    const otp_type = document.getElementById("otp-type");
    if (username.value != "" && email.value != "" && phone.value != "" && password.value != "" && confirm_password.value != "" && (otp.value != "" || otp_type.value != "")) {
        SendRegister().then((response)=>{
            if (response.status_code === 200) {
                window.location.replace(response.data.forward);
            } else if (response.status_code === 201) {
                username.disabled = true;
                email.disabled = true;
                phone.disabled = true;
                password.disabled = true;
                confirm_password.disabled = true;
                otp_type.disabled = true;
                otp.disabled = false;
                otp.style.visibility = "visible"
                otp.style.position = "relative";
                otp_type.style.visibility = "hidden"
                otp_type.style.position = "absolute";
                regbtn.textContent = "DAFTAR"
            } else {
                return response.json().then(data => {
                    console.log('Error:', data.message);
                });
            }
        }).catch((err)=>{
            alert(err)
        })
    } else {
        alert("data wajib di isi!")
    }

    // const secretKey = sessionStorage.getItem("SecretKey");
    // if (!secretKey) {
    //     console.log('Secret key is missing');
    //     return;
    // }

    // const nama = document.getElementById("nama").value;
    // const umur = document.getElementById("umur").value;
    // const bb = document.getElementById("bb").value;
    // const tinggi = document.getElementById("tinggi").value;
    // const jenis_kelamin = document.getElementById("jenis_kelamin").value;
    // const data = JSON.stringify({
    //     nama: nama,
    //     umur: umur,
    //     bb: bb,
    //     tinggi: tinggi,
    //     jenis_kelamin:jenis_kelamin,
    // });

    // try {
    //     const keyHex = CryptoJS.enc.Base64.parse(secretKey);
    //     const encryptedData = CryptoJS.AES.encrypt(data, keyHex, {
    //         mode: CryptoJS.mode.ECB,
    //         padding: CryptoJS.pad.Pkcs7
    //     }).toString();

    //     fetch('/input/send', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({ data: encryptedData })
    //     })
    //     .then(response => {
    //         if (response.status === 200) {
    //             response.json().then(res => {
    //                 window.location.replace(`/dashboard/${res.data.uuid}`);  // Redirect to /dashboard if status is 200
    //             })
    //         } else {
    //             return response.json().then(data => {
    //                 console.log('Error:', data.data.message);
    //             });
    //         }
    //     })
    //     .catch((error) => {
    //         console.log('Error:', error);
    //     });
    // } catch (e) {
    //     console.log('Error encrypting data:', e);
    // }
});
