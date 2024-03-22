// Capture HTML content
// const htmlContent = document.documentElement.outerHTML;

// Send HTML to Python backend
const serverUrl = 'http://localhost:5000/'

function displayData(data){
    const container = document.getElementById('Processed Evidence');
    data.forEach(event => {
        for (const [description, sources] of Object.entries(event)) {
            const eventDiv = document.createElement('div');
            eventDiv.classList.add('article');
            const descriptionHeader = document.createElement('h2');
            descriptionHeader.textContent = description;
            eventDiv.appendChild(descriptionHeader);

            sources.forEach(source => {
                for (const [url, articles] of Object.entries(source)) {
                    const sourceLink = document.createElement('a');
                    sourceLink.href = url;
                    sourceLink.textContent = url;
                    eventDiv.appendChild(sourceLink);

                    articles.forEach(article => {
                        for (const [headline, details] of Object.entries(article)) {
                            const headlineElement = document.createElement('h3');
                            headlineElement.textContent = headline;
                            eventDiv.appendChild(headlineElement);

                            const detailsParagraph = document.createElement('p');
                            detailsParagraph.textContent = JSON.stringify(details, null, 2);
                            eventDiv.appendChild(detailsParagraph);
                        }
                    });
                }
            });
            container.appendChild(eventDiv);
        }
    })
}

function displayData2(data){
    const container = document.getElementById('Processed Evidence');
    length = data.length;
    container.innerText = " ";
    
    for (i=0; i<length; i++){
        // TO DO
        container.innerText += JSON.stringify(data[i]) + "\n\n";

    }
}

// This is what helps display info on the extension
// fetch(serverUrl).then(response => response.json()).then(data => {
//     // process and display data in your extension UI
//     console.log('Data start: ', data);
//     // const dataContainer = document.getElementById('articleBriefContainer'); // should return container object
//     // error in this area
//     const dataContainer = document.getElementById('Processed Evidence');
//     console.log('Data Container: ', dataContainer);
//     // dataContainer.innerText = JSON.stringify(data);
//     dataContainer.innerText = data;
//     // displayData2(JSON.stringify(data));
//     // const dataTemp = JSON.stringify(data);
//     // const temp = JSON.parse(data);
//     // displayData(data);
//     // console.log('Data: ', data);
//     console.log('Data: ', data);
// }).catch(error => {
//     console.error('Error: ', error);
// });



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
                const dataContainer = document.getElementById('Processed Evidence');
                dataContainer.innerText = 'Processing...';
                fetch(serverUrl.concat('retrieve_evidence')).then(response => response.json()).then(data => {
                    // const dataContainer = document.getElementById('Processed Evidence');
                    // dataContainer.innerText = JSON.stringify(data);
                    displayData2(data);
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
// function fetchClaimInput(){
//     var claimInput = document.getElementById("claimInput").value;
//     console.log("Fetched claim input: ", claimInput);
//     document.getElementById("claimInput").value = ""; // clear input field
//     // send claimInput to Python backend
//     fetch(serverUrl.concat('process_claim'), {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({claim: claimInput})
//     }).then(response => {
//         console.log('Claim sent to Python backend');
//     }).catch(error => {
//         console.error('Error sending claim: ', error);
//     });
// }

// document.getElementById("demo").addEventListener("click", myFunction);
// document.getElementById("checkClaimButton").addEventListener("click", fetchClaimInput);


