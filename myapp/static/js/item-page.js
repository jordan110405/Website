document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    var query = document.getElementById('search-bar').value;

    fetch(`/search/${query}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Store the search results in sessionStorage
        sessionStorage.setItem('searchResults', JSON.stringify(data));
        // Redirect to the /item page
        window.location.href = `/item`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
