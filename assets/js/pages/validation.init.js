!function () {
    "use strict";
    window.addEventListener("load", function () {
        var t = document.getElementsByClassName("needs-validation");
        Array.prototype.filter.call(t, function (e) {


            e.addEventListener("submit", function (t) {
                let email = document.getElementById('email').value,
                password = document.getElementById('password').value,
                username = document.getElementById('username').value,
                v = e.checkValidity();
                console.log(password)
                fetch('/auth/users/', {
            method: 'POST', headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'email': email,
                'password': password,
                'username': username
            })
        }).then(r => r.json())
                    .then(data => {
                    console.log(data)
                for (const i in data){
                    v = !1
                    document.getElementById(i).setAttribute('ari', true)
                    document.getElementById(i).nextElementSibling.innerText = `" ${data[i][0]} "`
                }}
                    )
                !1 === v && (t.preventDefault()), e.classList.add("was-validated")
            }, !1)
        })
    }, !1)
}();