let inputMessage = document.querySelector('#inputMessage')
let lobby = document.querySelector('.chatbox .lobby')
let unReadMessage = document.querySelector('#unRead')
var usernameUserFriend = ''

inputMessage.focus()

inputMessage.onkeyup = function (elmt) {
    if (elmt.keyCode === 13) {
        if (inputMessage.value != '') {
            chatFriend(inputMessage.value)
            if (document.getElementById('usernameFriend').innerText != '') {
                document.querySelector('.container .chatbox .lobby').innerHTML += chatBox(user, inputMessage.value)
            }
            inputMessage.value = ''
            scrollToBottom()
        }
    }
}

