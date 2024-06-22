const chatInput = document.querySelector(".chat-controls input")
const chatButton = document.querySelector(".chat-controls button")
const chatForm = document.querySelector(".chat-form")
const chatWindow = document.querySelector(".chat-window")

let socket = io()
let thisIsMyMessage = false

const sendMessage = (e) => {
    e.preventDefault()
    
    message = chatInput.value
    chatInput.value = ""

    thisIsMyMessage = true
    console.log(message)
    if (message) {
        socket.emit('message', message)
    }
    /*
    fetch('/endpoints', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
    },
        body: JSON.stringify({
            user: "userA",
            chatMessage: message,
        }),
    }).then(response => response.json())
    .then(data => console.log(data))
    */
}


socket.on('connect', () => {
    console.log("conectado con el servidor")
})

socket.on('disconnect', () => {
    console.log("desconectado temporalmente")
})

socket.on('response', (msg) => {

  console.log(msg)

  messageComponent = document.createElement('DIV')
  messageComponent.className = thisIsMyMessage ? "--right" : "--left"
  messageComponent.innerHTML = `<div class="chat-message --userA"><p>${msg.message}</p></div>`

  chatWindow.appendChild(messageComponent)
  thisIsMyMessage = false
})


chatForm.addEventListener("submit", sendMessage)
