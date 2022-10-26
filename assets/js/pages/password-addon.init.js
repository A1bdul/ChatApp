document.getElementById("password-addon").addEventListener("click", function () {
    var e = document.getElementById("password-input");
    "password" === e.type ? e.type = "text" : e.type = "password"
});

document.getElementById('login-form') && document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    let email = document.getElementById('email').value,
        password = document.getElementById('password-input').value;
    fetch('/auth/jwt/create', {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'email': email,
            'password': password
        })
    })
        .then(r => r.json())
        .then(data => {
            window.localStorage.setItem('token', data['access'])
            window.location.replace('/')
        })
        .catch(err => {
        })
})
