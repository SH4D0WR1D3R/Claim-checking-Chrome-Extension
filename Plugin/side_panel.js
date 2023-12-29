// Capture HTML content
// const htmlContent = document.documentElement.outerHTML;

// Send HTML to Python backend

fetch('http://localhost:5000/get_data').then(response => response.json()).then(data => {
    // process and display data in your extension UI - this isn't working
    // document.getElementById('evidenceContainer').innerText = JSON.stringify(data);
    const dataContainer = document.getElementById('evidenceContainer'); // should return container object
    dataContainer.innerText = JSON.stringify(data);
}).catch(error => {
    console.error('Error:', error);
});

