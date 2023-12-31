// chrome.runtime.onUpdated.addEventListener(function(message, sender, sendResponse) {
//     const {htmlContent} = message;
//     console.log("Running contentScript");
//     if (htmlContent) {
//         console.log("Received HTML content: ", htmlContent);
//         // handle HTML here
//     }
// });

window.addEventListener("load", fetchHTML, false);

function fetchHTML () {
    console.log("LOADED");
    console.log(window.Document.toString())
    // add code to fetch HTML from active tab
    // the below line doesnt work
    // probably because it's been modified from what was originally suggested
    const [tab] = chrome.tabs.query({active: true, currentWindow: true});
    const html = chrome.scripting.executeScript({
        target: {tabId: tab.id},
        function: () => document.documentElement.outerHTML
    });
    console.log('HTML content:', html[0].result);
}