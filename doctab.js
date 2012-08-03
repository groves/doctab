chrome.tabs.onCreated.addListener(function (newTab) {
  if (!/#doc$/.test(newTab.url)) return;
  chrome.tabs.query({url: "file://*"}, function(tabs) {
    for (var i = 0; i < tabs.length; i++) {
      if (tabs[i].id != newTab.id && /#doc$/.test(tabs[i].url)) chrome.tabs.remove(tabs[i].id);
    }
  });
});