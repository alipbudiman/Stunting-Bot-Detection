let status_conv = "mulai"
let last_input_type = "chat"

function CodeBox(content) {
    // let Content = content.replace(/```([\s\S]+)```/g, `<code>$1</code>`);
    // // Content = Content.replace(/`([^`]+)`/g, '<code>$1</code>');
    // return Content
    return content
}

function userInputResults() {
    if (last_input_type === 'chat') {
        return document.getElementById("userInput-chat");
    } else if (last_input_type === '6-input') {
        return document.getElementById("userInput-6-input");
    } else if (last_input_type === '2-input') {
        return document.getElementById("userInput-2-input");
    }
}

function showInput(inputType) {
    const inputChat = document.getElementById('userInput-chat');
    const input6 = document.getElementById('userInput-6-input');
    const input2 = document.getElementById('userInput-2-input');

    const btnsend = document.getElementById('sendmessage');

    inputChat.style.visibility = "hidden";
    inputChat.style.position = "absolute";

    input6.style.visibility = "hidden";
    input6.style.position = "absolute";

    input2.style.visibility = "hidden";
    input2.style.position = "absolute";

    // Tampilkan input yang dipilih
    if (inputType === 'chat' || inputType === 'end') {
        inputChat.style.visibility = "visible";
        inputChat.style.position = "relative";
        if (inputType === 'end') {
            inputChat.disabled = true;
            btnsend.textContent = "Detail";
        }
        return 
    } else if (inputType === '6-input') {
        input6.style.visibility = "visible";
        input6.style.position = "relative";
    } else if (inputType === '2-input') {
        input2.style.visibility = "visible";
        input2.style.position = "relative";
    }
}

function userMessage(message) {
    const chatLog = document.getElementById("chatLog");
    // Append user message to chat log
    var userMessage = document.createElement("div");
    userMessage.className = "chat-message user";
    userMessage.innerHTML = "<p>" + CodeBox(message) + "</p>";
    chatLog.appendChild(userMessage);
}

function botMessage(message, error) {
    const chatLog = document.getElementById("chatLog");
    const botMessage = document.createElement("div");
    botMessage.className = "chat-message bot";
    botMessage.style.whiteSpace = "pre-line"; // Apply white-space: pre-line CSS property

    let paragraph = "<p>"
    if (error) { paragraph = `<p style="color:red;">` }
    let msg = `<img src="/static/images/5226034.png" alt="Profile Picture" class="profile-pic">` + paragraph + CodeBox(message) + "</p>";
    botMessage.innerHTML = msg
    chatLog.appendChild(botMessage);
}

function sendMessage() {
    const userInput = userInputResults();
    const message = userInput.value;

    if (message !== "") {
        const chatLog = document.getElementById("chatLog");

        // Append user message to chat log
        const userMessage = document.createElement("div");
        userMessage.className = "chat-message user";
        userMessage.innerHTML = "<p>" + CodeBox(message) + "</p>";
        chatLog.appendChild(userMessage);

        // Clear user input
        userInput.value = "";

        // Generate bot response
        setTimeout(function () {
            const botMessage = document.createElement("div");
            botMessage.className = "chat-message bot";
            botMessage.style.whiteSpace = "pre-line"; // Apply white-space: pre-line CSS property
            botMessage.innerHTML = `<img src="/static/images/5226034.png" alt="Profile Picture" class="profile-pic">` + "<p>" + '<span class="loading-icon"></span> Memproses, Harap Tunggu ...';
            chatLog.appendChild(botMessage);
            if (status_conv != "mulai") {
                AskAi(message).then((results) => {
                    const message = results.data.message
                    status_conv = results.data.status
                    last_input_type = results.data.input
                    showInput(results.data.input)
                    botMessage.innerHTML = `<img src="/static/images/5226034.png" alt="Profile Picture" class="profile-pic">` + "<p>" + CodeBox(message) + "</p>";
                }).catch(riject => {
                    botMessage.innerHTML = `<img src="/static/images/5226034.png" alt="Profile Picture" class="profile-pic">` + `<p style="color:red">` + CodeBox(riject) + "</p>";
                })
            } else {
                if (message.toLowerCase() == "mulai") {
                    status_conv = "ensure"
                    const message = "apakah anak anda mudah mengalami penyakit infeksi. Contohnya, sering demam, muntah, diare, dan lainnya?"
                    botMessage.innerHTML = `<img src="/static/images/5226034.png" alt="Profile Picture" class="profile-pic">` + "<p>" + CodeBox(message) + "</p>";
                } else {
                    const message = "ketik <b>mulai</b> untuk memulai percakapan"
                    botMessage.innerHTML = `<img src="/static/images/5226034.png" alt="Profile Picture" class="profile-pic">` + "<p>" + CodeBox(message) + "</p>";
                }
            }

            // Scroll to the bottom of the chat log
            chatLog.scrollTop = chatLog.scrollHeight;

        }, 1000);
    }
}

function GetMessageHistory() {
    return new Promise((resolve, riject) => {
        $.ajax({
            type: "POST",
            url: host + "/chatbot/history",
            data: {
                "authToken": authToken,
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

function AskAi(message) {
    return new Promise((resolve, riject) => {
        $.ajax({
            type: "POST",
            url: `${window.location.href}/send/${status_conv}`,
            data: {
                "chat": message,
            },
            success: (response) => {
                resolve(response)
            },
            error: (xhr, status, error) => {
                try {
                    const err = JSON.parse(xhr.responseText)
                    riject(`[Error: ${err.status}] ${err.response}`)
                } catch (er) {
                    riject(`[Error: ${status}] ${error}`)
                }
            }
        });
    })
}

function LoadMessageHistory() {
    GetMessageHistory().then((results) => {
        if (results.status === 200) {
            results.metadata.chat.forEach((element) => {
                if (element.role === "user") {
                    userMessage(element.content)
                } else if (element.role == "assistant") {
                    botMessage(element.content, false)
                }
            })
        }
    }).catch((riject) => {
        if (!riject.startsWith('[Error: 400] History Chat Empty!')) {
            botMessage(riject, true)
        }
    })
    const element = document.getElementById('content');
    element.style.visibility = 'visible';
    sessionStorage.clear();
    setTimeout(() => {
        $('#load').fadeOut();
    }, 1500);
    setTimeout(() => {
        $('#content').fadeIn();
    }, 2000);
}

function handleUserInput(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function scrollToBottom() {
    const chatLog = document.getElementById("chatLog");
    chatLog.scrollTo(0, document.body.scrollHeight);
}

function getLastUrlPart() {
    const currentUrl = window.location.href;
    const parts = currentUrl.split('/');
    return parts.pop() || parts.pop();
}

document.addEventListener('DOMContentLoaded', function () {
    $('#load').show();
    $('#content').hide();
    // LoadMessageHistory();
    // Scroll to the bottom of the chat log
    setTimeout(scrollToBottom, 250);

});



var userInput = document.getElementById("userInput-chat");
userInput.addEventListener("keypress", handleUserInput);
var userInput6 = document.getElementById("userInput-6-input");
userInput6.addEventListener("keypress", handleUserInput);
var userInput2 = document.getElementById("userInput-2-input");
userInput2.addEventListener("keypress", handleUserInput);

const buttonmsg = document.getElementById("sendmessage")
buttonmsg.addEventListener('click', function () {
    if (buttonmsg.textContent.toLowerCase() == "kirim") {
        sendMessage();
    } else {
        const user_id = getLastUrlPart()
        window.location.replace(`/detail/${user_id}`)
    }
})


