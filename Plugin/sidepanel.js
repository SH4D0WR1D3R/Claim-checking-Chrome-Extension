// Capture HTML content
// const htmlContent = document.documentElement.outerHTML;

// Send HTML to Python backend

fetch('http://localhost:5000/').then(response => response.json()).then(data => {
    document.getElementById('dataContainer').innerText = JSON.stringify(data);
}).catch(error => {
    console.error('Error:', error);
});