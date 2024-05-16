// List of allowed websites (whitelist)
const allowedDomains = [
    "ys.learnus.org",
    "gmail.com",
    "mail.google.com"
  ];

const allowedDomainEndings = [
    ".gov",
    ".edu"
]

const maxAllowedTabs = 30;

const blockAllRule = {
    id: 1,
    priority: 2,
    action: { type: "block" },
    condition: {

    }
};

const allowRules = [];

allowedDomains.forEach((domain, index) => {
    let num = 100 + index;
    let website = '*' + domain + '*';
    allowRules.push({
        id: num,
        priority: 1,
        action: { type: "allow" },
        condition: {
            urlFilter: website
        }
    })       
});

allowedDomainEndings.forEach((domain, index) => {
    let num = 200 + index;
    let website = '*' + domain + '*';
    allowRules.push({
        id: num,
        priority: 1,
        action: { type: "allow" },
        condition: {
            urlFilter: website
        }
    })       
});

// function to limit tab count
function limitTabs() {
    chrome.tabs.query({}, tabs => {
        if (tabs.length > maxAllowedTabs) {
            const tabsToRemove = tabs.slice(maxAllowedTabs); // Get excess tabs
            tabsToRemove.forEach(tab => {
                chrome.tabs.remove(tab.id); // Close each excess tab
            });
        }
    });
}
  
  // Limits the number of tabs when user tries to open new tab
  chrome.tabs.onCreated.addListener(tab => {
    limitTabs()  
  });

  // Limits the number of tabs when chrome first starts
  chrome.runtime.onStartup.addListener(() => {
    limitTabs()
  });

  // adds network rules when the extension is installed
  chrome.runtime.onInstalled.addListener(() => {
    console.log('Extension installed.');

    const allowRulesIds = allowRules.map(rule => rule.id);
    console.log(allowRules)
    console.log(allowRulesIds)

    //updating the network request rules
    chrome.declarativeNetRequest.updateDynamicRules({
        
        // first, we block all websites
        //removeRuleIds: [1],
        //addRules: [blockAllRule],
        //removeRuleIds: allowRulesIds,
        //addRules: allowRules
    });
  });