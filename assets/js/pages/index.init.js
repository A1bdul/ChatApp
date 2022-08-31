var input, filter, ul, li, a, i, j, div;

function searchUser() {
    for (
        input = document.getElementById("serachChatUser"),
            filter = input.value.toUpperCase(),
            ul = document.querySelector(".chat-room-list"),
            li = ul.getElementsByTagName("li"),
            i = 0;
        i < li.length;
        i++
    ) {
        -1 < li[i].querySelector("p").innerText.toUpperCase().indexOf(filter)
            ? (li[i].style.display = "")
            : (li[i].style.display = "none");
    }
}

function searchContacts() {
    for (
        input = document.getElementById("searchContact"),
            filter = input.value.toUpperCase(),
            list = document.querySelector(".sort-contact"),
            li = list.querySelectorAll(".mt-3 li"),
            div = list.querySelectorAll(".mt-3 .contact-list-title"),
            j = 0;
        j < div.length;
        j++
    ) {
        var e = div[j];
        (txtValue = e.innerText),
            -1 < txtValue.toUpperCase().indexOf(filter)
                ? (div[j].style.display = "")
                : (div[j].style.display = "none");
    }
    for (i = 0; i < li.length; i++)
        (contactName = li[i]),
            (txtValue = contactName.querySelector("h5").innerText),
            -1 < txtValue.toUpperCase().indexOf(filter)
                ? (li[i].style.display = "")
                : (li[i].style.display = "none");
}

function searchContactOnModal() {
    for (
        input = document.getElementById("searchContactModal"),
            filter = input.value.toUpperCase(),
            list = document.querySelector(".contact-modal-list"),
            li = list.querySelectorAll(".mt-3 li"),
            div = list.querySelectorAll(".mt-3 .contact-list-title"),
            j = 0;
        j < div.length;
        j++
    ) {
        var e = div[j];
        (txtValue = e.innerText),
            -1 < txtValue.toUpperCase().indexOf(filter)
                ? (div[j].style.display = "")
                : (div[j].style.display = "none");
    }
    for (i = 0; i < li.length; i++)
        (contactName = li[i]),
            (txtValue = contactName.querySelector("h5").innerText),
            -1 < txtValue.toUpperCase().indexOf(filter)
                ? (li[i].style.display = "")
                : (li[i].style.display = "none");
}

function getLocation() {
    navigator.geolocation
        ? navigator.geolocation.getCurrentPosition(showPosition)
        : (x.innerHTML = "Geolocation is not supported by this browser.");
}

function showPosition(e) {
    x.innerHTML =
        "Latitude: " + e.coords.latitude + "<br>Longitude: " + e.coords.longitude;
}

function cameraPermission() {
    navigator.mediaDevices.getUserMedia
        ? navigator.mediaDevices
            .getUserMedia({video: !0})
            .then(function (e) {
                video.srcObject = e;
            })
            .catch(function (e) {
                console.log(e);
            })
        : console.log("No");
}

function audioPermission() {
    navigator.mediaDevices.getUserMedia({audio: !0}).then(function (e) {
        (window.localStream = e),
            (window.localAudio.srcObject = e),
            (window.localAudio.autoplay = !0);
    });
}

function themeColor(e) {
    var c = window.localStorage.getItem("color"),
        d = window.localStorage.getItem("image");
    document.querySelectorAll(".theme-img , .theme-color").forEach(function (r) {
        r.id == c && (r.checked = !0), r.id == d && (r.checked = !0);
        var e,
            t,
            a,
            s = document.querySelector("input[name=bgcolor-radio]:checked");
        s &&
        ((s = s.id),
            (e = document.getElementsByClassName(s)),
            (t = window
                .getComputedStyle(e[0], null)
                .getPropertyValue("background-color")),
            (a = document.querySelector(".user-chat-overlay")),
            "bgcolor-radio8" == s
                ? ((t = "#4eac6d"), (a.style.background = null))
                : (a.style.background = t),
            (rgbColor = t.substring(t.indexOf("(") + 1, t.indexOf(")"))),
            document.documentElement.style.setProperty("--bs-primary-rgb", rgbColor));
        var i,
            l,
            n = document.querySelector("input[name=bgimg-radio]:checked");
        n &&
        ((n = n.id),
            window.localStorage.setItem("image", n),
            (i = document.getElementsByClassName(n)),
        e &&
        ((l = window
            .getComputedStyle(i[0], null)
            .getPropertyValue("background-image")),
            (document.querySelector(".user-chat").style.backgroundImage = l))),
            r.addEventListener("click", function (e) {
                r.id == c && (r.checked = !0), r.id == d && (r.checked = !0);
                var t,
                    a,
                    s,
                    i = document.querySelector("input[name=bgcolor-radio]:checked");
                i &&
                ((i = i.id),
                (t = document.getElementsByClassName(i)) &&
                ((a = window
                    .getComputedStyle(t[0], null)
                    .getPropertyValue("background-color")),
                    (s = document.querySelector(".user-chat-overlay")),
                    "bgcolor-radio8" == i
                        ? ((a = "#4eac6d"), (s.style.background = null))
                        : (s.style.background = a),
                    (rgbColor = a.substring(a.indexOf("(") + 1, a.indexOf(")"))),
                    document.documentElement.style.setProperty(
                        "--bs-primary-rgb",
                        rgbColor
                    ),
                    window.localStorage.setItem("color", i)));
                var l,
                    n,
                    o = document.querySelector("input[name=bgimg-radio]:checked");
                o &&
                ((o = o.id),
                    window.localStorage.setItem("image", o),
                    (l = document.getElementsByClassName(o)),
                t &&
                ((n = window
                    .getComputedStyle(l[0], null)
                    .getPropertyValue("background-image")),
                    (document.querySelector(".user-chat").style.backgroundImage = n)));
            });
    });
}

var primaryColor = window
    .getComputedStyle(document.body, null)
    .getPropertyValue("--bs-primary-rgb");

let b,
    x,
    r,
    w = 0,
    S = [],
    E = 1;
document
    .querySelector("#audiofile-input")
    .addEventListener("change", function () {
        var a = document.querySelector(".file_Upload");
        r = document.querySelector("#audiofile-input").files[0];
        var e = new FileReader();
        e.readAsDataURL(r),
        a && a.classList.add("show"),
            e.addEventListener(
                "load",
                function () {
                    var e = r.name,
                        t = Math.round(r.size / 1e6).toFixed(2);
                    (a.innerHTML =
                        '<div class="card p-2 border mb-2 audiofile_pre d-inline-block position-relative">            <div class="d-flex align-items-center">                <div class="flex-shrink-0 avatar-xs ms-1 me-3">                    <div class="avatar-title bg-soft-primary text-primary rounded-circle">                        <i class="bx bx-headphone"></i>                    </div>                </div>                <div class="flex-grow-1 overflow-hidden">                <h5 class="font-size-14 text-truncate mb-1">' +
                        e +
                        '</h5>                  <input type="hidden" name="downloadaudiodata" value="' +
                        r +
                        '"/>                        <p class="text-muted text-truncate font-size-13 mb-0">' +
                        t +
                        'mb</p>                </div>                <div class="flex-shrink-0 ms-3">                    <div class="d-flex gap-2">                        <div>                        <i class="ri-close-line text-danger audioFile-remove"  id="remove-audioFile"></i>                        </div>                    </div>                </div>            </div>          </div>'),
                        (b = e),
                        (x = t),
                        removeAudioFile(),
                        (S[E] = r);
                },
                !1
            ),
            E++;
    });
let q,
    k,
    c,
    L = [],
    A = 1;
document
    .querySelector("#attachedfile-input")
    .addEventListener("change", function () {
        var a = document.querySelector(".file_Upload");
        (c = document.querySelector("#attachedfile-input").files[0]),
            (fr = new FileReader()),
            fr.readAsDataURL(c),
        a && a.classList.add("show"),
            fr.addEventListener(
                "load",
                function () {
                    var e = c.name,
                        t = Math.round(c.size / 1e6).toFixed(2);
                    (a.innerHTML =
                        '<div class="card p-2 border attchedfile_pre d-inline-block position-relative">            <div class="d-flex align-items-center">                <div class="flex-shrink-0 avatar-xs ms-1 me-3">                    <div class="avatar-title bg-soft-primary text-primary rounded-circle">                        <i class="ri-attachment-2"></i>                    </div>                </div>                <div class="flex-grow-1 overflow-hidden">                <a href="" id="a"></a>                    <h5 class="font-size-14 text-truncate mb-1">' +
                        e +
                        '</h5>                    <input type="hidden" name="downloaddata" value="' +
                        c +
                        '"/>                    <p class="text-muted text-truncate font-size-13 mb-0">' +
                        t +
                        'mb</p>                </div>                <div class="flex-shrink-0 align-self-start ms-3">                    <div class="d-flex gap-2">                        <div>                        <i class="ri-close-line text-muted attechedFile-remove"  id="remove-attechedFile"></i>                        </div>                    </div>                </div>            </div>          </div>'),
                        (q = e),
                        (k = t),
                        (L[A] = c),
                        removeAttachedFile();
                },
                !1
            ),
            A++;
    });
let C = [];
removeimg = 1;
document
    .querySelector("#galleryfile-input")
    .addEventListener("change", function () {
        var s = document.querySelector(".file_Upload");
        s.insertAdjacentHTML(
            "beforeend",
            '<div class="profile-media-img image_pre"></div>'
        );
        var i = document.querySelector(".file_Upload .profile-media-img");
        this.files &&
        [].forEach.call(this.files, function (e) {
            if (!/\.(jpe?g|png|gif)$/i.test(e.name))
                return alert(e.name + " is not an image");
            var t = new FileReader(),
                a = "";
            t.addEventListener("load", function () {
                removeimg++,
                s && s.classList.add("show"),
                    C.push(t.result),
                    (a +=
                        '<div class="media-img-list" id="remove-image-' +
                        removeimg +
                        '">          <a href="#">              <img src="' +
                        this.result +
                        '" alt="' +
                        e.name +
                        '" class="img-fluid">          </a>            <i class="ri-close-line image-remove" onclick="removeImage(`remove-image-' +
                        removeimg +
                        '`)"></i>          </div>'),
                    i.insertAdjacentHTML("afterbegin", a),
                    0;
            }),
                t.readAsDataURL(e);
        });
    });


function removeImage(e) {
    document.querySelector("#" + e).remove(),
    0 == document.querySelectorAll(".image-remove").length &&
    document.querySelector(".file_Upload").classList.remove("show");
}

function removeAttachedFile() {
    document.getElementById("remove-attechedFile") &&
    (document.getElementsByClassName("attechedFile-remove")[0],
        document
            .getElementById("remove-attechedFile")
            .addEventListener("click", function (e) {
                e.target.closest(".attchedfile_pre").remove();
            })),
        document
            .querySelector("#remove-attechedFile")
            .addEventListener("click", function () {
                document.querySelector(".file_Upload ").classList.remove("show");
            });
}

function removeAudioFile() {
    document.getElementById("remove-audioFile") &&
    (document.getElementsByClassName("audioFile-remove")[0],
        document
            .getElementById("remove-audioFile")
            .addEventListener("click", function (e) {
                e.target.closest(".audiofile_pre").remove();
            })),
        document
            .querySelector("#remove-audioFile")
            .addEventListener("click", function () {
                document.querySelector(".file_Upload ").classList.remove("show");
            });
}

themeColor(primaryColor);
!(function () {
    "use strict";
    var e, t;
    [].slice
        .call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        .map(function (t) {
            return new bootstrap.Tooltip(t);
        }),
        [].slice
            .call(document.querySelectorAll('[data-bs-toggle="popover"]'))
            .map(function (t) {
                return new bootstrap.Popover(t);
            }),
        (e = document.getElementsByTagName("body")[0]),
    (t = document.querySelectorAll(".light-dark")) &&
    t.forEach(function (t) {
        t.addEventListener("click", function (t) {
            e.hasAttribute("data-layout-mode") &&
            "dark" == e.getAttribute("data-layout-mode")
                ? document.body.setAttribute("data-layout-mode", "light")
                : document.body.setAttribute("data-layout-mode", "dark");
        });
    })
    Waves.init();
})();