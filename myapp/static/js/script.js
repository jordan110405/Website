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
    document.querySelector('.items').innerHTML = '';
  
    // Make an AJAX request to the Flask route
    fetch(`/get_items/${category}`)
      .then(response => response.json())
      .then(items => {
        // Display items
        items.forEach(item => {
          const itemElement = document.createElement('div');
          itemElement.textContent = item.name; // Assuming item object has a 'name' property
          document.querySelector('.items').appendChild(itemElement);
        });
      })
      .catch(error => console.error('Error fetching items:', error));
  }
  