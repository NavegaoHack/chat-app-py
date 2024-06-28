const chatInput = document.querySelector(".chat-controls input")
const chatButton = document.querySelector(".chat-controls button")
const chatForm = document.querySelector(".chat-form")
const chatWindow = document.querySelector(".chat-window")

const menuChats = document.querySelector(".chat-menu__chats")

console.log(chatInput)
console.log(chatButton)
console.log(chatForm)
console.log(chatWindow)

let socket = io()
let thisIsMyMessage = false
let whoami = null
let userSelected = false

/*const getUsers = async () => {
    const response = await fetch('http://localhost:5000/api/users/get-previous-messages', {
        method: 'GET',
        headers: {
            "content-type": "application/json"
        },
        body: JSON.stringify(1)
    })
    const userList = await response.json()
    console.log(userList)
}*/

const checkIfIsMyMessage = (user) => {
    thisIsMyMessage = (user == whoami.user)
    
    console.log(user, whoami.user, thisIsMyMessage)
}

const printChats = (userList) => {
    userList.forEach((user, i) => {
        let chatContact = document.createElement("DIV")
        chatContact.className = `chat-menu__chat-contact ch-${i}`
        chatContact.dataset.userId = user.id
        chatContact.dataset.userName = user.username
        chatContact.innerHTML = `<p>${user.username[0].toUpperCase()}</p>`

        console.log(chatContact)
        menuChats.appendChild(chatContact)

    });
}

const printMessages = (messageList) => {
    messageList.forEach(message => {
        createMessage(message.username, message.message, message.created_at)
    })
}

const getUsers = async () => {
    const response = await fetch('http://localhost:5000/api/users/get-users-list', {
        method: 'GET',
        headers: {
            "content-type": "application/json"
        },
    })

    const userList = await response.json()
    printChats(userList)
}

const getPreviousMessages = async () => {
    const response = await fetch('http://localhost:5000/api/users/get-previous-messages', {
        method: 'GET',
        headers: {
            "content-type": "application/json"
        }//,
        //body: JSON.stringify({"chat-id": chatId})
    })

    const chatMessages = await response.json()
    printMessages(chatMessages)

}

const sendMessage = (e) => {
    e.preventDefault()
    
    const message = chatInput.value
    chatInput.value = ""

    let response = {
        userId: whoami.id,
        message: message
    }

    thisIsMyMessage = true
    if (message.replace(/\s/g, '') != "") {
        socket.emit('chat-message', response)
    }
}

const openChat = (e) => {
    if (userSelected) return

    socket.emit("connected-user", e.target.parentNode.classList[1])
    e.target.parentNode.classList.add("--connected")
    whoami = {
        user: e.target.parentNode.dataset.userName,
        id: e.target.parentNode.dataset.userId
    }
    console.log(whoami)
    userSelected = true
    getPreviousMessages()
}

const createMessage = (user, message, date) => {
  checkIfIsMyMessage(user)
  const messageComponent = document.createElement('DIV')
  
  const datePrinted = new Date(date)
  const amOrPm = (Math.floor(datePrinted.getHours() / 12) < 1) ? "AM" : "PM"
  
  const hours = datePrinted.getHours() % 12 || 12
  const minutes = datePrinted.getMinutes()

  const strDate = `${hours}:${minutes} ${amOrPm}`
   

  messageComponent.className = thisIsMyMessage  ? "--right" : "--left"

  messageComponent.innerHTML = `
  <div class="chat-message --userA">
      <div class="chat-message__time-user ${thisIsMyMessage ? "--t-right" : "--t-left"}">
        <p>${strDate}</p><div><p>${user[0].toUpperCase()}</p></div>
      </div>
      <div class="chat-message__inner">
          <p>${message}</p>
      </div>
  </div>
  `
  chatWindow.prepend(messageComponent)
  thisIsMyMessage = false
}

getUsers()

socket.on('broadcast-connected-user', (class_element) => {
    console.log(class_element)
    document.querySelector(`.${class_element}`).classList.add("--connected")
})

socket.on('broadcast-message', (response) => {
  console.log(response)
  createMessage(response.username, response.message, response.created_at)
})

menuChats.addEventListener("click", openChat)
chatForm.addEventListener("submit", sendMessage)
