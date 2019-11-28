function connectFriend(username) {
    if (userFriend == '') {
        usernameUserFriend = username
        console.log(usernameUserFriend)
        userFriend = new WebSocket('ws://{0}/ws/user/chat/{1}'.format(window.location.host, username))
        unReadMessage.innerHTML = ''
    } else {
        if (usernameUserFriend != username) {
            usernameUserFriend = username
            userFriend.close()
            userFriend = new WebSocket('ws://{0}/ws/user/chat/{1}'.format(window.location.host, username))
            unReadMessage.innerHTML = ''
        }
    }

    enableUserFriend()
}

function selectUser(username) {
    let usernameFriend = document.getElementById('usernameFriend')
    usernameFriend.innerHTML = username
    usernameFriend.style.visibility = 'visible'
    usernameFriend.style.transition = 'all 0.5s'
    usernameFriend.style.marginLeft = '0px'

    connectFriend(username)
}

function active(username) {
    let user = document.querySelector('.chatbox__user-list .user[username = "' + username + '"]')
    if (user != null) {
        user.setAttribute("class", "chatbox__user--active user")
    }
}

function nonactive(username) {
    let user = document.querySelector('.chatbox__user-list .user[username = "' + username + '"]')
    if (user != null) {
        user.setAttribute("class", "chatbox__user--busy user")
    }
}

function chatBox(username, message) {
    let position = ''
    if (username != user) {
        position = 'chatbox__right'
    } else {
        position = 'chatbox__left'
    }
    let chatBoxHtml = ''
    + '<div class="chatbox__messages {0}">'.format(position)
        + '<div class="chatbox__messages__user-message">'
            + '<div class="chatbox__messages__user-message--ind-message">'
                + '<p class="name">{0}</p>'.format(username)
                + '<br/>'
                + '<p class="message">{0}</p>'.format(message)
            + '</div>'
        + '</div>'
    + '</div>'

    return chatBoxHtml
}

function addChat(html) {
    document.querySelector('.container .chatbox .lobby').innerHTML += html
}

function scrollToBottom(params) {
    lobby.scrollTo({top: lobby.scrollHeight, behavior: 'smooth'})
}