let usernameLogin = ''
let userFriend = ''
let listUser = []
let user_online = new WebSocket('ws://{0}/ws/user/online/'.format(window.location.host))

let userWS = new WebSocket('ws://{0}/ws/user/chat/{1}'.format(window.location.host, user))

user_online.onopen = function () {
    user_online.send(
        JSON.stringify({
            'type_message': 'user_join',
            'value': user,
            'from': user
        })
    )
}

// recive message from other user
user_online.onmessage = function (returnData) {
    returnData = JSON.parse(returnData.data)
    
    if (returnData['type_message'] == 'user_join') {
        active(returnData['value'])
        listUser.push(returnData['value'])
        
        user_online.send(
            JSON.stringify({
                'type_message': 'get_user_online',
                'value': user,
                'from': user
            })
        )
    }
    if (returnData['type_message'] == 'get_user_online') {
        active(returnData['value'])
        listUser.push(returnData['value'])
    }
    if (returnData['type_message'] == 'user_disconnect') {
        // listUser.remove(returnData['value'])
        let newList = []
        let number = 0
        listUser.forEach(lsUser => {
            if (lsUser == returnData['value'] && number == 0) {
                number += 1
            } else {
                newList.push(lsUser)
            }
        })
        listUser = newList
        if (listUser.includes(returnData['value']) != true) {
            nonactive(returnData['value'])
        }
    }
}

user.onclose = function (e) {
    console.error('Chat socket closed unexpectedly')
}

userWS.onopen = function () {
    
}

userWS.onmessage = function (returnData) {
    returnData = JSON.parse(returnData.data)
    if (returnData['type_message'] == 'chat_friend') {
        if (returnData['from'] == usernameUserFriend) {
            lobby.innerHTML += chatBox(returnData['from'], returnData['value'])
            scrollToBottom()
        } else {
            if (unReadMessage.innerHTML == '') {
                unReadMessage.innerHTML = 1
            } else {
                unReadMessage.innerHTML = parseInt(unReadMessage.innerHTML) + 1
            }
        }
    }
}


function enableUserFriend() {
    userFriend.onopen = function () {
        userFriend.send(
            JSON.stringify({
                'type_message': 'history_chat',
                'value': '{0} - {1}'.format(user, usernameUserFriend)
            })
        )
    }
    
    userFriend.onmessage = function (returnData) {
        data = JSON.parse(returnData.data)
        if (data['type_message'] == 'history_chat') {
            document.querySelector('.container .chatbox .lobby').innerHTML = ''
            if (data['value'] != 'None' && data['value']['chat'].length != 0) {
                data['value']['chat'].forEach(chat => {
                    let username = chat['from']
                    let message = chat['value']
                    addChat(chatBox(username, message))
                })
                lobby.scrollTo({top: lobby.scrollHeight, behavior: 'smooth'})
            } 
        }
    }
}

function chatFriend(message) {
    userFriend.send(
        JSON.stringify({
            'type_message': 'chat_friend',
            'value': message,
            'user': '{0} - {1}'.format(user, usernameUserFriend)
        })
    )
}