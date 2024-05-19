document.addEventListener('DOMContentLoaded', function() {
    fetchAllItems();

    document.getElementById('search-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        var query = document.getElementById('search-bar').value;

        fetch(`/service/search/${query}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Store the search results in sessionStorage
            sessionStorage.setItem('searchResults', JSON.stringify(data));
            // Display search results
            displayItems(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Add event listeners for category selection
    document.querySelectorAll('.category').forEach(category => {
        category.addEventListener('click', function() {
            const categoryType = this.textContent.trim().toLowerCase();
            fetchItems(categoryType);
        });
    });
});

function fetchAllItems() {
    fetch(`/get_all_items_service`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Display all items
        displayItems(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function fetchItems(category) {
    fetch(`/service/get_items/${category}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Display items based on selected category
        displayItems(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayItems(items) {
    const productsContainer = document.querySelector('.products');
    productsContainer.innerHTML = '';

    items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.classList.add('product-item');
        itemElement.id = `item${item.id}`;

        itemElement.innerHTML = `
            <div class="product-items">
                <h2>${item.name}</h2>
                <img src="/static/uploads/${item.picture}" alt="Item Picture" height="200">
                <h3><strong>${item.blue}</strong> blue caps</h3>
                <p>${item.details}</p>
            </div>
        `;

        itemElement.addEventListener('click', () => {
            window.location.href = `/service/${item.id}`;
        });

        productsContainer.appendChild(itemElement);
    });
}


function openPopup() {
    const popup = document.getElementById('login-signup-popup');
    popup.style.display = 'block';
}

// Function to close the popup
function closePopup() {
    const popup = document.getElementById('login-signup-popup');
    popup.style.display = 'none';
}