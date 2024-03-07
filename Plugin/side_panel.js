// Capture HTML content
// const htmlContent = document.documentElement.outerHTML;

// Send HTML to Python backend
const serverUrl = 'http://localhost:5000/'

// This is what helps display info on the extension
fetch(serverUrl).then(response => response.json()).then(data => {
    // process and display data in your extension UI
    console.log('Data start: ', data);
    const dataContainer = document.getElementById('articleBriefContainer'); // should return container object
    // error in this area
    console.log('Data Container: ', dataContainer);
    dataContainer.innerText = JSON.stringify(data);
    // console.log('Data: ', data);
    console.log('Data: ', data);
}).catch(error => {
    console.error('Error: ', error);
});



// NEED A SEPARATE PROCESS TO DISPLAY RESULTS IN EVIDENCECONTAINER
// fetch(serverUrl.concat('process_html')).then(response => response.json()).then(data => {
//     const dataContainer = document.getElementById('evidenceContainer');
//     dataContainer.innerText = JSON.stringify(data);
// }).catch(error => {
//     console.error('Error: ', error);
// });

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
                const dataContainer = document.getElementById('evidenceContainer');
                dataContainer.innerText = 'Processing...';
                fetch(serverUrl.concat('retrieve_evidence')).then(response => response.json()).then(data => {
                    const dataContainer = document.getElementById('evidenceContainer');
                    dataContainer.innerText = JSON.stringify(data);
                    // NEED TO FORMAT NICELY - i love you - josh
                    // JSON.PARSE
                    // turn stuff into classes 
                }).catch(error => {
                    console.error('Error: ', error);
                });
            }).catch(error => {
                console.error('Error sending HTML content: ', error);
            });
        });
    }
});


// check if checkClaimButton has been clicked
// if so, send contents of claimInput to Python backend
function fetchClaimInput(){
    var claimInput = document.getElementById("claimInput").value;
    console.log("Fetched claim input: ", claimInput);
    document.getElementById("claimInput").value = ""; // clear input field
    // send claimInput to Python backend
    fetch(serverUrl.concat('process_claim'), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({claim: claimInput})
    }).then(response => {
        console.log('Claim sent to Python backend');
    }).catch(error => {
        console.error('Error sending claim: ', error);
    });
}

// document.getElementById("demo").addEventListener("click", myFunction);
document.getElementById("checkClaimButton").addEventListener("click", fetchClaimInput);