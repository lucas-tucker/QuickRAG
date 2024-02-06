function enable_app(enableIt) { // option page
    chrome.storage.local.get(['settings'], function (result) {
        if (enableIt) {
            chrome.contextMenus.create({
                title: 'Candice',
                id: 'Cand', // you'll use this in the handler function to identify this context menu item
                contexts: ['selection'],
            });
            result.settings.enableAddKw = true;
        } else {
            result.settings.enableAddKw = false;
        }

        chrome.storage.local.set({'settings': result.settings});
    });
}
  
// handle extension installation event
chrome.runtime.onInstalled.addListener(function (details) { 

    if (details.reason === chrome.runtime.OnInstalledReason.INSTALL){
        chrome.contextMenus.create({
            title: 'Candice',
            id: 'Cand', 
            contexts: ['selection'],
        });
        chrome.storage.local.set({'settings': settings});

    }else{

        chrome.storage.local.get(['settings'], function(result){
            var settings = result.settings;
            enable_app(settings.enableAddKw);
        });
    }

});


chrome.contextMenus.onClicked.addListener(function getword(info, tab) {
    if (info.menuItemId === "Cand") {
        // Open the extension popup window
        var linkUrl = info.linkUrl; // this is the highlighted text
        chrome.storage.local.set({linkUrl: linkUrl}, function() {
            chrome.windows.create({
                url: chrome.runtime.getURL("popup.html"), 
                type: "popup",
                width: 400, 
                height: 600 
            });
        });
        fetch('http://localhost:8000', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({type: 'linkUrl', data: linkUrl})
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            console.log('Success:', data);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }
});









