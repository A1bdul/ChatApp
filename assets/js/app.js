!(function () {
    fetch('user-error', {
        method: 'GET'
    })
        .then(r => r.json())
        .then(data => {
            for (const contacts in data) {
                if (data.hasOwnProperty(contacts)) {
                    let contact = data[contacts];
                    let i = `<div class="mt-3">
<div class="contact-list-title">
                                    ${contacts}
                                    </div>
                                    <ul class="list-unstyled contact-list">`
                    for (const user in contact) {
                        if (contact.hasOwnProperty(user)) {
                            i += (`<li>
                            <div>
                                <h5 class="font-size-14 m-0" style="cursor:pointer;">${contact[user].first_name} ${contact[user].last_name}</h5>
                            </div>
                        </li>`)
                        }
                    }
                    i += (` </ul>
                                </div>`);
                    document.getElementById('contactList').insertAdjacentHTML('beforeend', i)
                }
            }
        })
    
    fetch('/user-api', {
        method: 'GET',
    })
        .then(res => res.json())
        .then(main => {
            document.querySelectorAll('.user-name').forEach(link => link.innerHTML = main.first_name + ' ' + main.last_name)
            document.querySelectorAll('.user-email').forEach(link => link.innerHTML = main.email)
            let avatar = main.profile.avatar ? main.profile.avatar : '/assets/images/users/user-dummy-img.jpg'
            document.querySelectorAll('.user-image').forEach(link => link.src = avatar)
            document.querySelectorAll('.user-about').forEach(link => link.innerHTML = main.bio)
            fetch('/api/all-room', {
                method: 'GET'
            })
                .then(r => r.json())
                .then(room => {
                        for (const chat in room) {
                            if (chat === 'usersList' || chat === 'favourite_users') {
                                chatList(chat, room[chat], main)
                            }
                        }
                        let group_chat = room.channelList,
                            rooms = Object.assign(room.favourite_users, room.usersList)
                        console.log(rooms)
                        document.getElementById("empty-conversation").style.display = "block";
                        for (const chat in group_chat) {
                            if (group_chat.hasOwnProperty(chat)) {
                                let e = group_chat[chat]
                                var a = e.messagecount
                                        ? '<div class="flex-shrink-0 ms-2"><span class="badge badge-soft-dark rounded p-1">' +
                                        e.messagecount +
                                        "</span></div>"
                                        : "",
                                    s = e.messagecount
                                        ? '<a href="javascript: void(0);" class="unread-msg-user">'
                                        : '<a href="javascript: void(0);">';
                                document.getElementById("channelList").innerHTML +=
                                    '<li id="' +
                                    chat +
                                    '" data-name="channel">                ' +
                                    s +
                                    '                     <div class="d-flex align-items-center">                        <div class="flex-shrink-0 avatar-xs me-2">                            <span class="avatar-title rounded-circle bg-soft-light text-dark">#</span>                        </div>                        <div class="flex-grow-1 overflow-hidden">                            <p class="text-truncate mb-0">' +
                                    e.name +
                                    "</p>                        </div>                        <div>" +
                                    a +
                                    "</div>                        </div>                </a>            </li>";

                            }
                        }
                        window.addEventListener("DOMContentLoaded", function () {
                            let e = document.querySelector(
                                "#chat-conversation .simplebar-content-wrapper"
                            );
                            e.scrollTop = e.scrollHeight;
                        });

                        let profile_info = document.querySelector(".user-profile-sidebar"),
                            i = document.getElementById("chatinputmorecollapse");
                        f()

                        function p() {
                            let t = document
                                    .querySelector('.remove')
                                    .querySelector("#chat-conversation .simplebar-content-wrapper"),
                                a = document.getElementsByClassName("chat-conversation-list")[0]
                                    ? document
                                        .querySelector('.remove')
                                        .getElementsByClassName("chat-conversation-list")[0].scrollHeight -
                                    window.innerHeight +
                                    250
                                    : 0;
                            a && t.scrollTo({top: a, behavior: "smooth"});
                        }

                        document.body.addEventListener("click", function () {
                            new bootstrap.Collapse(i, {toggle: !1}).hide();
                        }),
                        i &&
                        i.addEventListener("shown.bs.collapse", function () {
                            new Swiper(".chatinput-links", {
                                slidesPerView: 3,
                                spaceBetween: 30,
                                breakpoints: {
                                    768: {slidesPerView: 4},
                                    1024: {slidesPerView: 6},
                                },
                            });
                        }),
                            document
                                .querySelectorAll(".contact-modal-list .contact-list li")
                                .forEach(function (e) {
                                    e.addEventListener("click", function () {
                                        e.classList.toggle("selected");
                                    });
                                }),
                            document.body.addEventListener("click", function () {
                                new bootstrap.Collapse(i, {toggle: !1}).hide();
                            }),
                        i &&
                        document
                            .querySelectorAll(".contact-modal-list .contact-list li")
                            .forEach(function (e) {
                                e.addEventListener("click", function () {
                                    e.classList.toggle("selected");
                                });
                            })

                        let chats = document.querySelectorAll('.users-chatlist');
                        chats.forEach(function (e) {
                            e.addEventListener('click', () => {
                                conversatonSettings(e)
                                const user = e.id;
                                conversatonSettings('users', rooms[user])
                                const is_user = (main.username !== rooms[user]['user1'].username) ? rooms[user]['user1'] : rooms[user]['user2'];
                                let a = is_user["first_name"],
                                    n = is_user['avatar'] ? is_user['avatar'] : '/assets/images/users/user-dummy-img.jpg';

                                (document.querySelector(
                                    ".user-profile-sidebar .user-name"
                                ).innerHTML = a),
                                    (document
                                        .getElementById("channel-chat")
                                        .querySelector(
                                            ".text-truncate .user-profile-show"
                                        ).innerHTML = a),
                                    (document.querySelector(
                                        ".user-profile-desc .text-truncate"
                                    ).innerHTML = a),
                                    (document.querySelector(
                                        ".audiocallModal .text-truncate"
                                    ).innerHTML = a),
                                    (document.querySelector(
                                        ".videocallModal .text-truncate"
                                    ).innerHTML = a);
                                (document.querySelectorAll('.user2-email').forEach(link => link.innerHTML = is_user.email))
                                let s = is_user["avatar"];
                                s
                                    ? (document
                                        .querySelector(".user-own-img .profile.avatar-sm")
                                        .querySelector(".user-own-img .avatar-sm")
                                        .setAttribute("src", s),
                                        document
                                            .querySelector(".user-profile-sidebar .profile-img")
                                            .setAttribute("src", s),
                                        document
                                            .querySelector(".audiocallModal .img-thumbnail")
                                            .setAttribute("src", s),
                                        document
                                            .querySelector(".videocallModal .videocallModal-bg")
                                            .setAttribute("src", s))
                                    : (document
                                        .querySelector(".user-own-img .avatar-sm")
                                        .setAttribute("src", n),
                                        document
                                            .querySelector(".user-profile-sidebar .profile-img")
                                            .setAttribute("src", n),
                                        document
                                            .querySelector(".audiocallModal .img-thumbnail")
                                            .setAttribute("src", n),
                                        document
                                            .querySelector(".videocallModal .videocallModal-bg")
                                            .setAttribute("src", n));
                                connectSocket('users', is_user.username, main.username)
                            })
                        })
                        let groups = document.querySelectorAll('#channelList li')
                        groups.forEach(function (e) {
                            e.addEventListener('click', () => {
                                const user = e.id;
                                conversatonSettings('group', group_chat[user])
                                let a = group_chat[user].name;
                                (document
                                    .getElementById("channel-chat")
                                    .querySelector(
                                        ".text-truncate .user-profile-show"
                                    ).innerHTML = a)
                                connectSocket('group', group_chat[user].id, main.username)
                            })
                        })
                    }
                )
        });


    document.getElementById("emoji-btn").addEventListener("click", function () {
        setTimeout(function () {
            var e,
                t = document.getElementsByClassName("fg-emoji-picker")[0];
            !t ||
            ((e = window.getComputedStyle(t)
                    ? window.getComputedStyle(t).getPropertyValue("left")
                    : "") &&
                ((e = (e = e.replace("px", "")) - 40 + "px"), (t.style.left = e)));
        }, 0);
    });
})();

function chatList(type, rooms, main) {
    for (const user in rooms) {
        if (rooms.hasOwnProperty(user)) {
            const is_user = (main.username !== rooms[user]['user1'].username) ? rooms[user]['user1'] : rooms[user]['user2'];
            const a = is_user["avatar"]
                    ? '<img src="' +
                    is_user["avatar"] +
                    '" class="rounded-circle avatar-xs" alt=""><span class="user-status"></span>'
                    : '<div class="avatar-xs"><span class="avatar-title rounded-circle bg-primary text-white"><span class="username">' + is_user["first_name"][0] + "" + is_user["last_name"][0] + '</span><span class="user-status"></span></span></div>',
                s = rooms[user]['unread'] ?
                    '<div class="ms-auto"><span class="badge badge-soft-dark rounded p-1">' + rooms[user]["unread"] + '</span></div>' : '',
                i = '<a href="javascript: void(0);" class="unread-msg-user">',
                l = 2 === rooms[user]['id'] ? "active" : "";
            document.getElementById(`${type}`).insertAdjacentHTML('afterbegin', '<li class="users-chatlist chatlist' + rooms[user]['id'] + '" id=' +
                user +
                ' data-name="direct-message">                  ' +
                i +
                '                   <div class="d-flex align-items-center">                      <div class="chat-user-img online align-self-center me-2 ms-0">                          ' +
                a +
                '                      </div>                      <div class="overflow-hidden">                          <p class="text-truncate mb-0">' +
                is_user["first_name"] +
                "  " +
                is_user["last_name"] +
                "</p>                      </div>                      " +
                s +
                "                  </div>              </a>        </li>"
            );
        }
    }
}


function connectSocket(type, chatId, user2) {
    let url = type === 'group' ? `ws://${window.location.host}/ws/group/${chatId}` : `ws://${window.location.host}/ws/${chatId}`,
        message_url = type === 'group' ? 'api/group-message/' + chatId : `api/room-messages/${chatId}`,
        socket = new WebSocket(url);
    fetch(message_url, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            for (const i in data) {
                if (data.hasOwnProperty(i)) {
                    let message = data[i]
                    chatArrange(message, user2)
                }
            }
        });
    let l = document.querySelector("#chatinput-form"),
        g = document.querySelector("#chat-input"),
        u = document.getElementById('submit-btn')

    socket.onmessage = function (e) {
        let message = JSON.parse(e.data);
        if (message.type === 'typing' && message.user !== user2) {
            document.getElementById('activity').innerText = 'typing..'
            setTimeout(function () {
                document.getElementById('activity').innerText = ''
            }, 3000)
        } else if (message.command === 'private_chat') {
            chatArrange(message, user2)
        }
    }
    l.addEventListener('submit', (e) => {
        e.preventDefault()
    })
    u.addEventListener('click', (e) => {
        e.preventDefault();
        let value = g.value,
            o = document.querySelector(".image_pre"),
            r = document.querySelector(".attchedfile_pre"),
            replycard = document.querySelector('.replyCard'),
            reply_id = replycard ? replycard.id : null,
            reply_user = replycard ? replycard.getAttribute('data-user') : null;
        c = document.querySelector(".audiofile_pre");
        if (o !== null) {
            socket.send(JSON.stringify({
                command: 'private_chat_with_image',
                images: C,
                msg: value,
                reply_id: reply_id,
                reply_user: reply_user
            }))
        } else if (r !== null) {
            socket.send(JSON.stringify({
                command: 'private_chat_with_file',
                files: L,
                msg: value,
                reply_id: reply_id,
                reply_user: reply_user
            }))
        } else if (c !== null) {
            socket.send(JSON.stringify({
                command: 'private_chat_with_audio',
                audio: S,
                msg: value,
                reply_id: reply_id,
                reply_user: reply_user
            }))
        } else if (value) {
            socket.send(JSON.stringify({
                command: 'private_chat',
                msg: value,
                reply_id: reply_id,
                reply_user: reply_user
            }))
        }

        (g.value = ""),
        document.querySelector(".image_pre") &&
        document.querySelector(".image_pre").remove(),
            (document.getElementById("galleryfile-input").value = ""),
        document.querySelector(".attchedfile_pre") &&
        document.querySelector(".attchedfile_pre").remove(),
            (document.getElementById("attachedfile-input").value = ""),
        document.querySelector(".audiofile_pre") &&
        document.querySelector(".audiofile_pre").remove(),
            (document.getElementById("audiofile-input").value = ""),
            document.getElementById("close_toggle").click();
    })
    document.getElementById("chat-input").focus();

    g.addEventListener('keypress', () => {
        socket.send(JSON.stringify({
            command: 'typing'
        }))
    })
}

function chatArrange(message, user2) {

    function p() {
        let t = document
                .querySelector('.remove')
                .querySelector("#chat-conversation .simplebar-content-wrapper"),
            a = document.getElementsByClassName("chat-conversation-list")[0]
                ? document
                    .querySelector('.remove')
                    .getElementsByClassName("chat-conversation-list")[0].scrollHeight -
                window.innerHeight +
                250
                : 0;
        a && t.scrollTo({top: a, behavior: "smooth"});
    }

    function H(e, t, a, s, i, j) {
        let l = '<div class="ctext-wrap">',
            f = j && message.sender.username !== j.sender.username ? j.sender.first_name : 'You:';
        q = j ? `<div class="replymessage-block mb-0 d-flex align-items-start">
    <div class="flex-grow-1"><h5 class="conversation-name">${f}</h5><p class="mb-0">${j.msg}</p></div>
    <div class="flex-shrink-0">
        <button type="button" class="btn btn-sm btn-link mt-n2 me-n3 font-size-18"></button>
    </div>
</div>` : '';
        if (t !== "")
            l +=
                '<div class="ctext-wrap-content">' + q + '<p class="mb-0  ctext-content mt-1 p-1"  id=' +
                e +
                '>' +
                t +
                "</p></div>";
        else if (a && 0 < a.length) {
            for (l += '<div class="message-img mb-0">', T = 0; T < a.length; T++)
                l +=
                    '<div class="message-img-list"><div><a class="popup-img d-inline-block" href="' +
                    a[T] +
                    '">                <img src="/assets/images/users/user-dummy-img.jpg" alt="" class="rounded border"></a></div><div class="message-img-link"><ul class="list-inline mb-0"><li class="list-inline-item dropdown"><a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">                      <i class="bx bx-dots-horizontal-rounded"></i></a><div class="dropdown-menu">                  <a class="dropdown-item d-flex align-items-center justify-content-between" href="' +
                    a[T] +
                    '" download>Download <i class="bx bx-download ms-2 text-muted"></i></a><a class="dropdown-item d-flex align-items-center justify-content-between"  href="#" data-bs-toggle="collapse" data-bs-target=".replyCollapse">Reply <i class="bx bx-share ms-2 text-muted"></i></a>                  <a class="dropdown-item d-flex align-items-center justify-content-between" href="#" data-bs-toggle="modal" data-bs-target=".forwardModal">Forward <i class="bx bx-share-alt ms-2 text-muted"></i></a>                  <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Bookmark <i class="bx bx-bookmarks text-muted ms-2"></i></a>                  <a class="dropdown-item d-flex align-items-center justify-content-between delete-image" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a></div>              </li>          </ul>        </div>      </div>';
            l += "</div>";
        } else
            0 < s.length &&
            (l +=
                '<div class="ctext-wrap-content">            <div class="p-3 border-primary border rounded-3">            <div class="d-flex align-items-center attached-file">                <div class="flex-shrink-0 avatar-sm me-3 ms-0 attached-file-avatar">                    <div class="avatar-title bg-soft-primary text-primary rounded-circle font-size-20">                        <i class="ri-attachment-2"></i>                    </div>                </div>                <div class="flex-grow-1 overflow-hidden">                    <div class="text-start">                        <h5 class="font-size-14 mb-1">design-phase-1-approved.pdf</h5>                        <p class="text-muted text-truncate font-size-13 mb-0">12.5 MB</p>                    </div>                </div>                <div class="flex-shrink-0 ms-4">                    <div class="d-flex gap-2 font-size-20 d-flex align-items-start">                        <div>                            <a href="#" class="text-muted">                                <i class="bx bxs-download"></i>                            </a>                        </div>                    </div>                </div>             </div>            </div>            </div>            <div class="dropdown align-self-start message-box-drop">                <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">                    <i class="ri-more-2-fill"></i>                </a>                <div class="dropdown-menu">                  <a class="dropdown-item d-flex align-items-center justify-content-between"  href="' +
                s +
                '" download>Download <i class="bx bx-download ms-2 text-muted"></i></a>                  <a class="dropdown-item d-flex align-items-center justify-content-between" href="#" data-bs-toggle="collapse" data-bs-target=".replyCollapse">Reply <i class="bx bx-share ms-2 text-muted"></i></a>                  <a class="dropdown-item d-flex align-items-center justify-content-between" href="#" data-bs-toggle="modal" data-bs-target=".forwardModal">Forward <i class="bx bx-share-alt ms-2 text-muted"></i></a>                  <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Bookmark <i class="bx bx-bookmarks text-muted ms-2"></i></a>                  <a class="dropdown-item d-flex align-items-center justify-content-between delete-item" href="#">Delete <i class="bx bx-trash text-muted ms-2"></i></a>                </div>            </div>');
        return (
            !0 === i &&
            (l +=
                '<div class="dropdown align-self-start message-box-drop">                <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">                    <i class="ri-more-2-fill"></i>                </a>                <div class="dropdown-menu">                    <a class="dropdown-item d-flex align-items-center justify-content-between reply-message" href="#" id="reply-message-' +
                e +
                '" data-bs-toggle="collapse" data-bs-target=".replyCollapse">Reply <i class="bx bx-share ms-2 text-muted"></i></a>                    <a class="dropdown-item d-flex align-items-center justify-content-between" href="#" data-bs-toggle="modal" data-bs-target=".forwardModal">Forward <i class="bx bx-share-alt ms-2 text-muted"></i></a>                    <a class="dropdown-item d-flex align-items-center justify-content-between copy-message" href="#" id="copy-message-' +
                e +
                '">Copy <i class="bx bx-copy text-muted ms-2"></i></a>                    <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Bookmark <i class="bx bx-bookmarks text-muted ms-2"></i></a>                    <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Mark as Unread <i class="bx bx-message-error text-muted ms-2"></i></a>                    <a class="dropdown-item d-flex align-items-center justify-content-between delete-item" href="#">Delete <i class="bx bx-trash text-muted ms-2"></i></a>                </div>            </div>'),
                (l += "</div>")
        );
    }

    let a, i, s;
    a = message.sender.username === user2 ? ' right' : ' left';
    s = message.reply ? message.reply : null;
    (i =
        '<li class="chat-list' +
        a +
        '" id=" chat-' +
        message.id +
        '">                        <div class="conversation-list">');
    if (message.sender.username !== user2) {
        i += message.sender.profile.avatar ? `<div class="chat-avatar"><img src="${message.sender.profile.avatar}" alt=""></div>` : `<div class="chat-avatar"><img src="/assets/images/users/user-dummy-img.jpg" alt=""></div>`;
    }
    (i += '<div class="user-chat-content">'),
        (i += H(
            message.id,
            message.msg,
            message.images,
            message.files,
            message.dropdown,
            message.reply
        )),
        (i +=
            '<div class="conversation-name"><small class="text-muted time">' +
            message.created_at +
            '</small> <span class="text-success check-message-icon"><i class="bx bx-check-double"></i></span></div>'),
        (i += "</div>                </div>            </li>");
    document.querySelector('.chat-conversation-list').insertAdjacentHTML('beforeend', i);
    document.querySelector(`#reply-message-${message.id}`).addEventListener('click', (s) => {
        let i = document.querySelector("#reply"),
            o = document.querySelector("#close_toggle");

        i.classList.add("show")
        i.setAttribute('id', `${message.id}`)
        i.setAttribute('data-user', `${message.sender.username}`)
        o.addEventListener("click", function () {
            i.classList.remove("show");
        });
        document.getElementById("chat-input").focus();
        let e = document.getElementById(`${message.id}`).innerText,
            a = message.sender.username !== user2 ? message.sender.first_name : 'You:';
        document.querySelector('#reply_text').innerText = e;
        document.querySelector('#reply_user').innerText = a;
    })
    p()
}

function conversatonSettings(type, data) {
    let a = type === 'group' ? `<div id="channel-chat" class="remove position-relative">
                        <div class="p-3 p-lg-4 user-chat-topbar">
                            <div class="row align-items-center">
                                <div class="col-sm-4 col-8">
                                    <div class="d-flex align-items-center">
                                        <div class="flex-shrink-0 d-block d-lg-none me-3">
                                            <a href="javascript: void(0);" class="user-chat-remove font-size-18 p-1"><i class="bx bx-chevron-left align-middle"></i></a>
                                        </div>
                                        <div class="flex-grow-1 overflow-hidden">
                                            <div class="d-flex align-items-center">                            
                                                <div class="flex-shrink-0 chat-user-img online user-own-img align-self-center me-3">
                                                <span class="avatar-title rounded-circle bg-soft-light text-dark">#</span>                         
                                                </div>
                                                <div class="flex-grow-1 overflow-hidden">
                                                    <h6 class="text-truncate mb-0 font-size-18"><a href="#" class="user-profile-show text-reset">Design Phase 2</a></h6>
                                                    <p class="text-truncate text-muted mb-0"><small>24 Members</small></p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-8 col-4">
                                    <ul class="list-inline user-chat-nav text-end mb-0">                                        
                                        <li class="list-inline-item">
                                            <div class="dropdown">
                                                <button class="btn nav-btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                    <i class='bx bx-search'></i>
                                                </button>
                                                <div class="dropdown-menu p-0 dropdown-menu-end dropdown-menu-lg">
                                                    <div class="search-box p-2">
                                                        <input type="text" class="form-control" placeholder="Search..">
                                                    </div>
                                                </div>
                                            </div>
                                        </li>

                                        <li class="list-inline-item d-none d-lg-inline-block me-2 ms-0">
                                            <button type="button" class="btn nav-btn user-profile-show">
                                                <i class='bx bxs-info-circle'></i>
                                            </button>
                                        </li>

                                        <li class="list-inline-item">
                                            <div class="dropdown">
                                                <button class="btn nav-btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                    <i class='bx bx-dots-vertical-rounded' ></i>
                                                </button>
                                                <div class="dropdown-menu dropdown-menu-end">
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none user-profile-show" href="#">View Profile <i class="bx bx-user text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none" href="#" data-bs-toggle="modal" data-bs-target=".audiocallModal">Audio <i class="bx bxs-phone-call text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none" href="#" data-bs-toggle="modal" data-bs-target=".videocallModal">Video <i class="bx bx-video text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center" href="#">Archive <i class="bx bx-archive text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center" href="#">Muted <i class="bx bx-microphone-off text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center" href="#">Delete <i class="bx bx-trash text-muted"></i></a>
                                                </div>
                                            </div>
                                        </li>                                        
                                    </ul>                                    
                                </div>
                            </div>
                            <div class="alert alert-warning alert-dismissible topbar-bookmark fade show p-1 px-3 px-lg-4 pe-lg-5 pe-5" role="alert">
                                <div class="d-flex align-items-start bookmark-tabs">
                                    <div class="tab-list-link">
                                        <a href="#" class="tab-links" data-bs-toggle="modal" data-bs-target=".pinnedtabModal"><i class="ri-pushpin-fill align-middle me-1"></i> 10 Pinned</a>
                                    </div>
                                    <div>
                                        <a href="#" class="tab-links border-0 px-3" data-bs-toggle="tooltip" data-bs-trigger="hover" data-bs-placement="bottom" title="Add Bookmark"><i class="ri-add-fill align-middle"></i></a>
                                    </div>
                                </div>
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div>
                        </div>
                        <!-- end chat user head -->

                        <!-- start chat conversation -->

                        <div class="chat-conversation p-3 p-lg-4" id="chat-conversation" data-simplebar>
                            <ul class="list-unstyled chat-conversation-list" id="channel-conversation">       
                            </ul>
                        </div>
                        <div class="alert alert-warning alert-dismissible copyclipboard-alert px-4 fade show " id="copyClipBoardChannel" role="alert">
                            message copied
                        </div>
                        <!-- end chat conversation end -->
                        </div>` : `<div id="channel-chat" class="remove position-relative">
                    <div class="p-3 p-lg-4 user-chat-topbar">
                        <div class="row align-items-center">
                            <div class="col-sm-4 col-8">
                                <div class="d-flex align-items-center">
                                    <div class="flex-shrink-0 d-lg-none me-3">
                                        <a href="javascript: void(0);" class="user-chat-remove font-size-18 p-1"><i class="bx bx-chevron-left align-middle"></i></a>
                                    </div>
                                    <div class="flex-grow-1 overflow-hidden">
                                        <div class="d-flex align-items-center">
                                            <div class="flex-shrink-0 chat-user-img online user-own-img align-self-center me-3">
                                                <img class="rounded-circle avatar-sm" alt="" src=>
                                            </div>
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h6 class="text-truncate mb-0 font-size-18"><a href="#" class="user-profile-show text-reset"></a></h6>
                                                <p class="text-truncate text-muted mb-0"><small id="activity"></small></p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-sm-8 col-4">
                                <ul class="list-inline user-chat-nav text-end mb-0">
                                        <li class="list-inline-item">
                                            <div class="dropdown">
                                                <button class="btn nav-btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                    <i class='bx bx-search'></i>
                                                </button>
                                                <div class="dropdown-menu p-0 dropdown-menu-end dropdown-menu-lg">
                                                    <div class="search-box p-2">
                                                        <input type="text" class="form-control" placeholder="Search.." id="searchChatMessage">
                                                    </div>
                                                </div>
                                            </div>
                                        </li>

                                        <li class="list-inline-item d-none d-lg-inline-block me-2 ms-0">
                                            <button type="button" class="btn nav-btn" data-bs-toggle="modal" data-bs-target=".audiocallModal">
                                                <i class='bx bxs-phone-call' ></i>
                                            </button>
                                        </li>

                                        <li class="list-inline-item d-none d-lg-inline-block me-2 ms-0">
                                            <button type="button" class="btn nav-btn" data-bs-toggle="modal" data-bs-target=".videocallModal">
                                                <i class='bx bx-video' ></i>
                                            </button>
                                        </li>

                                        <li class="list-inline-item d-none d-lg-inline-block me-2 ms-0">
                                            <button type="button" class="btn nav-btn user-profile-show">
                                                <i class='bx bxs-info-circle' ></i>
                                            </button>
                                        </li>

                                        <li class="list-inline-item">
                                            <div class="dropdown">
                                                <button class="btn nav-btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                    <i class='bx bx-dots-vertical-rounded' ></i>
                                                </button>
                                                <div class="dropdown-menu dropdown-menu-end">
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none user-profile-show" href="#">View Profile <i class="bx bx-user text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none" href="#" data-bs-toggle="modal" data-bs-target=".audiocallModal">Audio <i class="bx bxs-phone-call text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none" href="#" data-bs-toggle="modal" data-bs-target=".videocallModal">Video <i class="bx bx-video text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center" href="#">Archive <i class="bx bx-archive text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center" href="#">Muted <i class="bx bx-microphone-off text-muted"></i></a>
                                                    <a class="dropdown-item d-flex justify-content-between align-items-center" href="#">Delete <i class="bx bx-trash text-muted"></i></a>
                                                </div>
                                            </div>
                                        </li>
                                    </ul>
                            </div>
                        </div>
                        <div class="alert alert-warning alert-dismissible topbar-bookmark fade show p-1 px-3 px-lg-4 pe-lg-5 pe-5" role="alert">
                            <div class="d-flex align-items-start bookmark-tabs">
                                <div class="tab-list-link">
                                    <a href="#" class="tab-links" data-bs-toggle="modal" data-bs-target=".pinnedtabModal"><i class="ri-pushpin-fill align-middle me-1"></i> 10 Pinned</a>
                                </div>
                                <div>
                                    <a href="#" class="tab-links border-0 px-3" data-bs-toggle="tooltip" data-bs-trigger="hover" data-bs-placement="bottom" title="Add Bookmark"><i class="ri-add-fill align-middle"></i></a>
                                </div>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    </div>
                    <!-- end chat user head -->
    
                    <!-- start chat conversation -->
                        <div class="chat-conversation p-3 p-lg-4 " id="chat-conversation" data-simplebar>
                        <ul class="list-unstyled chat-conversation-list" id="users-conversation">
                        </ul>
                    </div>
                    <!-- end chat conversation end -->
                    </div>`;
    document.getElementById("empty-conversation").innerHTML = (a);
    document.getElementById(
        "channel-chat"
    ).style.display = "block";
    document.getElementById("chat-input-section").style.display =
        "block";
    document.getElementById("chat-input").focus();
    f();
    F();
}

function f() {
    let f = document.getElementsByClassName("user-chat");
    document
        .querySelectorAll(".chat-user-list li a")
        .forEach(function (e) {
            e.addEventListener("click", function (e) {
                f.forEach(function (e) {
                    e.classList.add("user-chat-show");
                });
                let t = document.querySelector(".chat-user-list li.active");
                t && t.classList.remove("active"),
                    this.parentNode.classList.add("active");
            });

        }),
        document
            .querySelectorAll(".sort-contact ul li")
            .forEach(function (e) {
                e.addEventListener("click", function (e) {
                    f.forEach(function (e) {
                        e.classList.add("user-chat-show");
                    });
                });
            }),
        document
            .querySelectorAll(".user-chat-remove")
            .forEach(function (e) {
                e.addEventListener("click", function (e) {
                    f.forEach(link => link.classList.remove('user-chat-show'));
                });
            });
    let t = document.querySelector(".user-profile-sidebar");
    document.querySelectorAll(".user-profile-show").forEach(function (e) {
        e.addEventListener("click", function (e) {
            t.classList.toggle("d-block");
        });
    })

}

function F() {
    GLightbox({selector: ".popup-img", title: !1});
}
