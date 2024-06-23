const chatInput = document.querySelector(".chat-controls input")
const chatButton = document.querySelector(".chat-controls button")
const chatForm = document.querySelector(".chat-form")
const chatWindow = document.querySelector(".chat-window")

console.log(chatInput)
console.log(chatButton)
console.log(chatForm)
console.log(chatWindow)

let socket = io()
let thisIsMyMessage = false

const sendMessage = (e) => {
    e.preventDefault()
    
    const message = chatInput.value
    chatInput.value = ""

    thisIsMyMessage = true
    if (message.replace(/\s/g, '') != "") {
        socket.emit('chat-message', message)
    }
}

const autoScroolToDown = () => {
  console.log(chatWindow.scrollTop)
}

/*
                <div class="--left">
                    <div class="chat-message --userA">
                        <div class="chat-message__time-user --t-left"><p>10:00AM</p><div><p>u</p></div></div>
                        <div class="chat-message__inner">
                            <p>message we Lorem, ipsum dolor sit amet consectetur adipisicing elit. In non voluptatem ratione voluptatum neque tenetur minus quaerat necessitatibus enim optio temporibus aspernatur totam officia inventore, dignissimos illum! Architecto asperiores quod consequuntur sed! Cum suscipit, saepe ducimus quas deserunt rerum voluptates fugiat sunt doloremque, libero, magni ea ratione impedit. Pariatur, rem.</p>
                        </div>
                    </div>
                </div>
*/

socket.on('broadcast-message', (msg) => {

  autoScroolToDown()

  console.log(msg)
  const messageComponent = document.createElement('DIV')
  messageComponent.className = thisIsMyMessage ? "--right" : "--left"

  messageComponent.innerHTML = `
  <div class="chat-message --userA">
      <div class="chat-message__time-user ${thisIsMyMessage ? "--t-right" : "--t-left"}">
        <p>10:00AM</p><div><p>u</p></div>
      </div>
      <div class="chat-message__inner">
          <p>${msg}</p>
      </div>
  </div>
  `
  chatWindow.prepend(messageComponent)
  thisIsMyMessage = false
})


chatForm.addEventListener("submit", sendMessage)
