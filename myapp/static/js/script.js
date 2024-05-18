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







function debounce(func, wait, immediate) {
  let timeout;
  return function() {
    const context = this;
    const args = arguments;
    const later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}


const apiKey = '0a3cfc11ac124345a8bdfc860029cbd2';
const inputField = document.getElementById('signup-location');

inputField.addEventListener('input', debounce(function() {
    const query = inputField.value;
    fetch(`https://api.opencagedata.com/geocode/v1/json?q=${query}&key=${apiKey}&types=city`)
        .then(response => response.json())
        .then(data => {
            const filteredSuggestions = data.results.filter(result => {
                // Check if 'components' includes 'road', indicating a street-level address
                return result.components && result.components.city;
            });

            const suggestions = filteredSuggestions.map(result => result.formatted);
            document.getElementById("locationDropdown").innerHTML = "";
            if (suggestions !== null) {
                suggestions.forEach(function(e) {
                    const option = document.createElement("h6");
                    option.textContent = e;
                    document.getElementById("locationDropdown").appendChild(option);

                    option.addEventListener("click", function() {
                        inputField.value = e;
                        document.getElementById("locationDropdown").innerHTML = "";
                    });
                });
            }
        })
        .catch(error => {
            console.error(error);
        });
}, 300));



fetch('/')
    .then(response => response.json())
    .then(data => {
        // Process the data and display it on the webpage
        const products = data.products;
        console.log(data.products);
        products.forEach(product => {
            const productDiv = document.createElement('div');
            productDiv.textContent = `Product ID: ${product.id}, Name: ${product.name}, Picture: ${product.picture},
            Pickup_location: ${product.pickup_location}, Contact_info: ${product.product_info}`;
            document.getElementById('product-list').appendChild(productDiv);
        });
    })
    .catch(error => console.log(error));


function itemClick(id) {
    window.location.href = "/" + id.toString();
}