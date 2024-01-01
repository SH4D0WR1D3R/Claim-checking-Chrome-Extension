// this file acts as an event handler

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // checks the message being received is the one with the html content
    if (message && message.action === 'getHTMLContent') {
        chrome.scripting.executeScript({
            // the target is the active tab - should be what is sent in with the message
            target: {tabId: sender.tab.id},
            // this function is run under the context of the web page (active tab)
            function: () => {
                return {html: document.documentElement.outerHTML};
            },  
        // (variable) => {} is a callback function
        }, (result) => {
            const htmlContent = result[0].result.html;
            sendResponse({htmlContent});
        });
        return true;
    }
});