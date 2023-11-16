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