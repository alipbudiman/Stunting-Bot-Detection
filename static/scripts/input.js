function SendInput(){
    return new Promise((resolve, riject)=>{
        const nama = document.getElementById("nama").value;
        const umur = document.getElementById("umur").value;
        const bb = document.getElementById("bb").value;
        const tinggi = document.getElementById("tinggi").value;
        const jenis_kelamin = document.getElementById("jenis_kelamin").value;
        $.ajax({
            type: "POST",
            url: "/input/send",
            data: {
                nama: nama,
                umur: umur,
                bb: bb,
                tinggi: tinggi,
                jenis_kelamin:jenis_kelamin,
            },
            success: (response) => {
                resolve(response)
            },
            error: (xhr, status, error) => {
                try {
                    const err = JSON.parse(xhr.responseText)
                    if (err.status_code == 500) {
                        window.location.reload("/login")
                    }
                    riject(`[Error: ${err.status_code}] ${err.message}`)
                } catch (er) {
                    riject(`[Error: ${status}] ${error}`)
                }
            }
        });
    })

}

document.getElementById("inputdata").addEventListener('click', () => {
    const nama = document.getElementById("nama").value;
    const umur = document.getElementById("umur").value;
    const bb = document.getElementById("bb").value;
    const tinggi = document.getElementById("tinggi").value;
    const jenis_kelamin = document.getElementById("jenis_kelamin").value;
    if (nama != "" && umur != "" && bb != "" && tinggi != "" && jenis_kelamin != "" && Number(bb) > 0 && Number(tinggi) > 0 ) {
        SendInput().then((response)=>{
            if (response.status_code === 200) {
                window.location.replace(`/dashboard/${response.data.uuid}`);
            } else {
                return response.json().then(data => {
                    console.log('Error:', data.data.message);
                });
            }
        }).catch((err)=>{
            alert(err)
        })
    } else {
        alert("data tidak boleh kosong!")
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
