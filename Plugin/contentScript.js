// this file is the one that can directly access the contents of the web page

// Send a message to the background script requesting HTML content
chrome.runtime.sendMessage({action: 'getHTMLContent'}, (response) => {
    if (response && response.htmlContent) {
        // Send the HTML content to the sidePanel.js file
        const port = chrome.runtime.connect({name: 'htmlContent'});
        port.postMessage({htmlContent: response.htmlContent});
    }
});
