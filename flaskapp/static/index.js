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
        socket.emit('chat-message', message)
    }
}


socket.on('broadcast-message', (msg) => {

  console.log(msg)

  messageComponent = document.createElement('DIV')
  messageComponent.className = thisIsMyMessage ? "--right" : "--left"
  messageComponent.innerHTML = `<div class="chat-message --userA"><p>${msg}</p></div>`

  chatWindow.appendChild(messageComponent)
  thisIsMyMessage = false
})


chatForm.addEventListener("submit", sendMessage)
