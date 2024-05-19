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

function fetchItems(category) {
    // Clear previous items
    const productsContainer = document.querySelector('.products');
    productsContainer.innerHTML = '';

    // Make an AJAX request to the Flask route based on the selected category
    fetch(`/get_items/${category}`)
      .then(response => response.json())
      .then(items => {
        // Display items
        items.forEach(item => {
          const itemElement = document.createElement('div');
          itemElement.classList.add('product-item'); // Add a CSS class for styling
          itemElement.id = `item${item.id}`; // Set the custom ID
          
          itemElement.innerHTML = `
            <div class="product-items">
            <h2>${item.name}</h2>
            <img src="static/uploads/${item.picture}" alt="Item Picture" height="200">
            <h3><strong>${item.blue}</strong> blue caps</h3>
            <p>${item.details}</p>
            </div>
          `;

          // Add click event listener
          itemElement.addEventListener('click', () => {
            itemClick(item.id);
          });

          productsContainer.appendChild(itemElement);
        });
      })
      .catch(error => console.error('Error fetching items:', error));
}




function itemClick(id) {
    window.location.href = "/" + id.toString();
}