// Define the debounce function
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Define the event handler function
const handlePageNumberUpdated = (pageNumber) => {
    console.log("tests");
    console.log(`Switched to page: ${pageNumber}`);
    fetch('/capture_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            page_number: pageNumber,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};

WebViewer({
    path: window.PDFJSExpressLibPath,
    initialDoc: window.PDFInitialDocPath,
    disabledElements: ["header", "annotation"],
}, document.getElementById('pdf-wrapper'))
    .then(instance => {
        instance.UI.setTheme('dark');
        instance.UI.disableFeatures([instance.UI.Feature.Print, instance.UI.Feature.Annotations]);

        const { documentViewer } = instance.Core;

        // Use debounce to wrap the event handler function
        documentViewer.addEventListener('pageNumberUpdated', debounce(handlePageNumberUpdated, 300));
    });
