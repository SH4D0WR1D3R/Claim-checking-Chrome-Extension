// chrome.tabs.onUpdated.addListener(async (tabID, info, tab) => {
//     chrome.sidePanel // lets user open side panel on clicking action toolbar
//         .setPanelBehavior({openPanelOnActionClick: true})
//         .catch((error) => console.error(error));
// });


// chrome.runtime.onInstalled.addListener(() => {
//     chrome.contextMenus.create({
//         id: 'openSidePanel',
//         title: 'Open side panel',
//         contexts: ['all']
//     });
// });

// chrome.contextMenus.onClicked.addListener((info, tab) => {
//     if (info.menuItemId === 'openSidePanel') {
//         chrome.sidePanel.open({windowId: tab.windowId});
//     }    
// });

// chrome.runtime.onInstalled.addListener(() => {
//     console.log('Extension Installed');
// });

// chrome.action.onClicked.addListener(async () => {
//     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true});
//     chrome.scripting.executeScript({
//         target: {tabId: tab.id},
//         function: () => {
//             const htmlContent = document.documentElement.outerHTML;
//             chrome.runtime.sendMessage({htmlContent});
//         }
//     });
//     console.log('HTML Content:', html[0].result);
// });



// chrome.webNavigation.onDOMContentLoaded.addListener(event => {
//     if (event.frameId === 0) {
//         chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
//             chrome.tabs.sendMessage(tabs[0].id, {action: 'startContentScript'});
//         });
//     }
// });
// chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
//     chrome.tabs.sendMessage(tabs[0].id, {action: 'startContentScript'});
// });