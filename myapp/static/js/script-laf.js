document.getElementById("logoImage").addEventListener("click", function() {
    window.location.href = "/";
});

function fetchIPAddress(apiKey, callback) {
    var request = new XMLHttpRequest();

    request.open('GET', `https://api.ipdata.co/?api-key=${apiKey}`);
    request.setRequestHeader('Accept', 'application/json');

    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const responseData = JSON.parse(this.responseText);
            callback(responseData);
        }
    };

    request.send();
}

function handleIPAddressResponse(responseData) {
    console.log(responseData.city);
}

//fetchIPAddress('62cf928590e8802fd1a2c82dc3051361ff1f044eaf0d546a8ef27d1d', handleIPAddressResponse);


function openPopup() {
    const element = document.getElementById("login-signup-popup")
    element.style.display = "flex";

    const element_foreach = document.querySelectorAll(".signup-login-textbox");
    element_foreach.forEach(element => {
        element.value = "";
        element.setAttribute("value", "");
    });
}

function closePopup() {
    document.getElementById("login-signup-popup").style.display = "none";
    const element_foreach = document.querySelectorAll(".signup-login-textbox");
    element_foreach.forEach(element => {
        element.value = "";
        element.setAttribute("value", "");
    });
}

const input = document.querySelectorAll(".signup-login-textbox");
input.forEach(input => {
    input.addEventListener("input", function() {
        input.setAttribute("value", input.value);
    });
});

function myProfilePopup() {
    document.getElementById("profile-popup").style.display = 'block';
    document.getElementById("profile-popup").style.position = 'absolute';
    document.getElementById("profile-popup").style.padding = '24px 24px 24px 16px';
}


function myProfilePopupOff() {
    document.getElementById("profile-popup").style.display = 'none';
}

function itemClick(id) {
    window.location.href = "/online-lost-and-found/" + id.toString();
}