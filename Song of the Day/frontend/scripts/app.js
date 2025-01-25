// This file contains the JavaScript code for the frontend application. 
// It handles user interactions, makes API calls to the backend, and updates the UI dynamically.

document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = 'http://localhost:5000/api'; // Adjust the URL as needed

    // Example function to fetch data from the backend
    async function fetchData() {
        try {
            const response = await fetch(`${apiUrl}/data`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    // Example function to update the UI with fetched data
    function updateUI(data) {
        const outputElement = document.getElementById('output');
        outputElement.innerHTML = JSON.stringify(data, null, 2);
    }

    // Call fetchData on page load
    fetchData();
});