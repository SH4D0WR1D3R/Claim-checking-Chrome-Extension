// Capture HTML content
// const htmlContent = document.documentElement.outerHTML;

// Send HTML to Python backend
const serverUrl = 'http://localhost:5000/'

fetch(serverUrl).then(response => response.json()).then(data => {
    // process and display data in your extension UI
    // document.getElementById('evidenceContainer').innerText = JSON.stringify(data);
    const dataContainer = document.getElementById('evidenceContainer'); // should return container object
    dataContainer.innerText = JSON.stringify(data);
}).catch(error => {
    console.error('Error: ', error);
});
// }).catch(error) {
//     console.error("Error: ", error);
// }
// });

// const htmlContent = document.documentElement.outerHTML;
// fetch(serverUrl.concat('/process_html'), {method: 'POST', headers: {
//     'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({html: htmlContent})
// }).then(response => response.json()).then(data => {
//     console.log('Response from Python:', data);
// }).catch(error => {
//     console.error('Error sending HTML to Python: ', error);
// });

// chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
//     chrome.tabs.executeScript(tabs[0].id, {code: 'document.documentElement.outerHTML'}, function(html) {
//         console.log('HTML content of the active tab:', html[0]);
//         // send HTML to backend using fetch
//     });
// });

// chrome.tabs.query({active: true, currentWindow: true}).then(function (tabs){
//     var activeTab = tabs[0];
//     var activeTabId = activeTab.id;
//     // return chrome.scripting
// })