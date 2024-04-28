// Capture HTML content
// const htmlContent = document.documentElement.outerHTML;

// Send HTML to Python backend
const serverUrl = 'http://localhost:5000/'

function displayData(data){
    const container = document.getElementById('Processed Evidence');
    length = data.length;
    container.innerText = " ";
    
    for (i=0; i<length; i++){
        container.innerText += JSON.stringify(data[i]) + "\n\n";
    }
}

// Listen for messages from contentScript.js
// this section of code is waiting for the html content of the active tab
chrome.runtime.onConnect.addListener((port) => {
    // checks the port name is the one with the html content
    if (port.name === 'htmlContent') {
        // when receive a message, grab the html content from said message
        port.onMessage.addListener((msg) => {
            const htmlContent = msg.htmlContent;
            console.log('HTML Content: ', htmlContent);
            fetch(serverUrl.concat('process_html'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({html: htmlContent})
            }).then(response => {
                console.log('HTML content sent to Python backend');
                const dataContainer = document.getElementById('Processed Evidence');
                dataContainer.innerText = 'Processing...';
                fetch(serverUrl.concat('retrieve_evidence')).then(response => response.json()).then(data => {
                    displayData(data);
                }).catch(error => {
                    console.error('Error: ', error);
                });
            }).catch(error => {
                console.error('Error sending HTML content: ', error);
            });
        });
    }
});

