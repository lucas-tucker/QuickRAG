function handle_addKw_change(enableIt) { // option page
    chrome.storage.local.get(['settings'], function (result) {
        if (enableIt) {
            chrome.contextMenus.create({
                title: 'Candice',
                id: 'Cand', // you'll use this in the handler function to identify this context menu item
                contexts: ['selection'],
            });
            result.settings.enableAddKw = true;
        } else {
            chrome.contextMenus.remove("addKw");
            result.settings.enableAddKw = false;
        }

        chrome.storage.local.set({'settings': result.settings});
    });
}
  
// handle extension installation event
chrome.runtime.onInstalled.addListener(function (details) { // when first installed, extension updated, browser updated

    if (details.reason === chrome.runtime.OnInstalledReason.INSTALL){

        var popupConfig = {
            // Pop-up window settings
            popup_width: 400,
            popup_height: 100,
        }
    
        // add context menu item
        chrome.contextMenus.create({
            title: 'Candice',
            id: 'Cand', // you'll use this in the handler function to identify this context menu item
            contexts: ['selection'],
        });
        chrome.storage.local.set({'settings': settings, 'popupConfig': popupConfig});

    }else{

        chrome.storage.local.get(['settings', 'popupConfig'], function(result){
            var settings = result.settings;
            var popupConfig = result.popupConfig;

            handle_addKw_change(settings.enableAddKw);
            handle_popupSize_change(popupConfig.popup_height, popupConfig.popup_width);
        });
    }

});


chrome.contextMenus.onClicked.addListener(function getword(info, tab) {
    if (info.menuItemId === "Cand") {
        // Open the extension popup window
        var linkUrl = info.linkUrl; // this is the highlighted text
        chrome.storage.local.set({linkUrl: linkUrl}, function() {
            chrome.windows.create({
                url: chrome.runtime.getURL("popup.html"), // replace "popup.html" with the path to your popup HTML file
                type: "popup",
                width: 400, // replace with your desired width
                height: 600 // replace with your desired height
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









