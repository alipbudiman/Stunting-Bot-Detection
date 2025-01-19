function LoginPost() {
    return new Promise((resolve, riject)=> {
        $.ajax({
            type: "POST",
            url: "/login/send",
            data: {
                "email": document.getElementById("email").value,
                "password":document.getElementById("password").value,
            },
            success: (response) => {
                resolve(response)
            },
            error: (xhr, status, error) => {
                try {
                    const err = JSON.parse(xhr.responseText)
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
    if (hide.textContent.toLowerCase() === 'jangan sembunyikan password') {
        password.type = 'text';
        hide.textContent = 'sembunyikan password'
    } else {
        password.type = 'password';
        hide.textContent = 'jangan sembunyikan password'
    }

})

document.getElementById("loginbtn").addEventListener('click', () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value
    if (email != "" && password != "") {
        LoginPost().then((response)=>{
            if (response.status_code == 200) {
                window.location.replace(response.data.forward);
            } else {
                alert(response.message)
            }
        }).catch((error)=> {
            alert(error)
        })
    } else {
        alert("Email / no telepon dan password tidak boleh kosong!")
    }
    

    // const secretKey = sessionStorage.getItem("SecretKey");
    // console.log(secretKey)
    // if (!secretKey) {
    //     console.error('Secret key is missing');
    //     return;
    // }

    // const username = document.getElementById("email").value;
    // const password = document.getElementById("password").value;
    // const data = JSON.stringify({
    //     email: username,
    //     password: password
    // });

    // try {
    //     const keyHex = CryptoJS.enc.Base64.parse(secretKey);
    //     const encryptedData = CryptoJS.AES.encrypt(data, keyHex, {
    //         mode: CryptoJS.mode.ECB,
    //         padding: CryptoJS.pad.Pkcs7
    //     }).toString();
    //     console.log('Encrypted Data:', encryptedData);

    //     fetch('/login/send', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({ data: encryptedData })
    //     })
    //     .then(response => {
    //         if (response.status === 200) {
    //             window.location.href = '/input'; 
    //         } else {
    //             return response.json().then(data => {
    //                 console.error('Error:', data.message);
    //             });
    //         }
    //     })
    //     .catch((error) => {
    //         console.error('Error:', error);
    //     });
    // } catch (e) {
    //     console.error('Error encrypting data:', e);
    // }
});
