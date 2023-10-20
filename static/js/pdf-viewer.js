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

// Function to initialize the WebViewer with a given file
let viewerInstance = null;

const initializeViewer = (file) => {
    if (viewerInstance) {
        viewerInstance.loadDocument(file);
    } else {
        WebViewer({
            path: window.PDFJSExpressLibPath,
            initialDoc: file,
            disabledElements: ["header", "annotation"],
        }, document.getElementById('pdf-wrapper'))
            .then(instance => {
                viewerInstance = instance;
                instance.UI.setTheme('dark');
                instance.UI.disableFeatures([instance.UI.Feature.Print, instance.UI.Feature.Annotations]);

                const { documentViewer } = instance.Core;
                console.log("TESTING THIS")
                documentViewer.addEventListener('pageNumberUpdated', debounce(handlePageNumberUpdated, 300));
            });
    }
};

// Initially, initialize the viewer with the default file
initializeViewer(window.PDFInitialDocPath);

// Set up the upload button click event listener
document.getElementById('upload-button').addEventListener('click', () => {
    document.getElementById('file-input').click();
});

// Set up the file input change event listener
document.getElementById('file-input').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload_file', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.status === 413) {
                throw new Error('File is too large.');
            }
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                // Optional delay before initializing the viewer
                setTimeout(() => {
                    initializeViewer(data.url);
                }, 1000);
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
