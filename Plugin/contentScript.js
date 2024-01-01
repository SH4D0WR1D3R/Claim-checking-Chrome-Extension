// chrome.runtime.onUpdated.addEventListener(function(message, sender, sendResponse) {
//     const {htmlContent} = message;
//     console.log("Running contentScript");
//     if (htmlContent) {
//         console.log("Received HTML content: ", htmlContent);
//         // handle HTML here
//     }
// });

// window.addEventListener("load", fetchHTML, false);

// function fetchHTML () {
//     console.log("LOADED");
//     console.log(window.Document.toString())
    // add code to fetch HTML from active tab
    // the below line doesnt work
    // probably because it's been modified from what was originally suggested
    // const [tab] = chrome.tabs.query({active: true, currentWindow: true});
    // const html = chrome.scripting.executeScript({
    //     target: {tabId: tab.id},
    //     function: () => document.documentElement.outerHTML
    // });
    // console.log('HTML content:', html[0].result);
    // chrome.tabs.getSelected - gets the tab selected
    // chrome.tabs.sendRequest - send request to the content script
    // chrome.extension.onRequest.addListener

    // error: Uncaught TypeError: Cannot read properties of undefined (reading 'query')
    // this error seems to occur when trying to access a property of an object which hasn't been defined yet
    // chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
    //     chrome.tabs.executeScript(tabs[0].id, {code: 'document.documentElement.outerHTML'}, function(html) {
    //         console.log('HTML content of the active tab:', html[0]);
    //         // send HTML to backend using fetch
    //     });
    // });

    // const [tab] = chrome.tabs.query({active: true, currentWindow: true});


//     console.log("Successful query")
    
    
// }
chrome.webNavigation.onDOMContentLoaded.addListener(event => {
    if (event.frameId === 0) {
        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: 'startContentScript'});
        });
    }
});

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse){
    if (message_action === 'startContentScript') {
        // how can i get the tab id from the received message
        const {tabId, msg_txt} = message;
        chrome.scripting.executeScript(tabId, {code: 'document.documentElement.outerHTML'}, function(html) {
            console.log('HTML content of the active tab:', html[0]);
            // send HTML to backend using fetch
        });
        
    }
});
