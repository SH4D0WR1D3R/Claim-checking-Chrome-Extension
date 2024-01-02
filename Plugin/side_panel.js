// Capture HTML content
// const htmlContent = document.documentElement.outerHTML;

// Send HTML to Python backend
const serverUrl = 'http://localhost:5000/'

fetch(serverUrl).then(response => response.json()).then(data => {
    // process and display data in your extension UI
    const dataContainer = document.getElementById('evidenceContainer'); // should return container object
    dataContainer.innerText = JSON.stringify(data);
}).catch(error => {
    console.error('Error: ', error);
});

// Listen for messages from contentScript.js
// this section of code is waiting for the html content of the active tab
chrome.runtime.onConnect.addListener((port) => {
    // checks the port name is the one with the html content
    if (port.name === 'htmlContent') {
        // when receive a message, grab the html content from said message
        port.onMessage.addListener((msg) => {
            const htmlContent = msg.htmlContent;
            console.log('HTML Content: ', htmlContent);
        });
    }
});