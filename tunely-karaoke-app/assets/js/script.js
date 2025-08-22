document.addEventListener('DOMContentLoaded', () => {
    // --- Hero Section Typing Effect ---
    const typingElement = document.getElementById('typing-effect');
    const phrases = ["Create stunning karaoke videos.", "For Hindi & Marathi songs.", "Powered by AI."];
    let phraseIndex = 0;
    let letterIndex = 0;
    let currentPhrase = "";
    let isDeleting = false;

    function type() {
        const fullPhrase = phrases[phraseIndex];
        if (isDeleting) {
            currentPhrase = fullPhrase.substring(0, letterIndex - 1);
            letterIndex--;
        } else {
            currentPhrase = fullPhrase.substring(0, letterIndex + 1);
            letterIndex++;
        }

        typingElement.textContent = currentPhrase;

        let typeSpeed = 150;
        if (isDeleting) {
            typeSpeed /= 2;
        }

        if (!isDeleting && letterIndex === fullPhrase.length) {
            typeSpeed = 2000; // Pause at end
            isDeleting = true;
        } else if (isDeleting && letterIndex === 0) {
            isDeleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            typeSpeed = 500; // Pause before new phrase
        }

        setTimeout(type, typeSpeed);
    }
    type();

    // --- Upload Functionality ---
    const uploadBox = document.getElementById('upload-box');
    const audioUpload = document.getElementById('audio-upload');
    const browseBtn = document.getElementById('browse-btn');
    const processBtn = document.getElementById('process-btn');
    const fileNameDisplay = document.getElementById('file-name');
    const loader = document.getElementById('loader');
    const loadingText = document.querySelector('.loading-text');


    browseBtn.addEventListener('click', () => audioUpload.click());

    ['dragover', 'dragenter'].forEach(eventName => {
        uploadBox.addEventListener(eventName, (e) => {
            e.preventDefault();
            uploadBox.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadBox.addEventListener(eventName, (e) => {
            e.preventDefault();
            uploadBox.classList.remove('dragover');
        });
    });

    uploadBox.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    audioUpload.addEventListener('change', (e) => {
        const files = e.target.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    function handleFile(file) {
        if (file && file.type.startsWith('audio/')) {
            fileNameDisplay.textContent = `File selected: ${file.name}`;
            processBtn.disabled = false;
        } else {
            fileNameDisplay.textContent = 'Please select a valid audio file.';
            processBtn.disabled = true;
        }
    }

    // --- Processing and API Call ---
    processBtn.addEventListener('click', async () => {
        if (!audioUpload.files[0]) {
            alert("Please select a file first.");
            return;
        }

        loader.style.display = 'flex';
        loadingText.textContent = 'Uploading your song...';

        const formData = new FormData();
        formData.append('file', audioUpload.files[0]);

        try {
            loadingText.textContent = 'Processing... this may take several minutes.';
            
            const response = await fetch('http://127.0.0.1:5000/api/process-karaoke', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                console.log("Success:", result);
                // Redirect to the result page, passing the video URL as a parameter
                window.location.href = `result.html?video=${encodeURIComponent(result.video_url)}`;
            } else {
                // If the server returns an error, display it
                throw new Error(result.error || 'An unknown error occurred.');
            }

        } catch (error) {
            console.error('Error:', error);
            loader.style.display = 'none';
            // Use a more user-friendly error display than alert in a real app
            alert(`Processing failed: ${error.message}`);
        }
    });
});
