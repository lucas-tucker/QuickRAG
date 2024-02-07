
// Author: Lucas Tucker

// handle extension installation event
chrome.runtime.onInstalled.addListener(function (details) { 
    chrome.contextMenus.create({ // this creates the right-click menu option
        title: 'QuickRAG',
        id: 'QuickRAG', 
        contexts: ['selection'],
    });

    if (details.reason === chrome.runtime.OnInstalledReason.INSTALL){
        chrome.storage.local.set({'settings': settings});
    }
});

chrome.contextMenus.onClicked.addListener(function getword(info, tab) {
    if (info.menuItemId === "QuickRAG") {
        // Open the extension popup window
        var linkUrl = info.linkUrl; // this is the highlighted text
        fetch('http://localhost:8000', {
            method: 'POST', // post the url data to the server
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({type: 'linkUrl', data: linkUrl})
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            chrome.storage.local.set({linkUrl: linkUrl}, function() {
                chrome.windows.create({
                    url: chrome.runtime.getURL("templates/popup.html"), 
                    type: "popup",
                    width: 400, 
                    height: 600 
                });
            });
            return response.json();
        }).then(data => {
            console.log('Success:', data);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }
});
