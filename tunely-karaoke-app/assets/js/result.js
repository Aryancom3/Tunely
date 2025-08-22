document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('karaoke-video');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const downloadBtn = document.getElementById('download-btn');
    const resultTitle = document.querySelector('.result-title');

    // --- Get video URL from the page's query parameter ---
    const params = new URLSearchParams(window.location.search);
    const videoUrlPath = params.get('video');

    if (videoUrlPath) {
        // Construct the full URL to the backend server
        const fullVideoUrl = `http://127.0.0.1:5000${videoUrlPath}`;
        
        video.src = fullVideoUrl;
        downloadBtn.href = fullVideoUrl;
    } else {
        resultTitle.textContent = "Could not find video.";
        playPauseBtn.disabled = true;
        downloadBtn.style.display = 'none';
    }


    function togglePlay() {
        if (video.paused || video.ended) {
            video.play();
        } else {
            video.pause();
        }
    }

    playPauseBtn.addEventListener('click', togglePlay);

    video.addEventListener('play', () => {
        playPauseBtn.textContent = 'Pause';
    });

    video.addEventListener('pause', () => {
        playPauseBtn.textContent = 'Play';
    });
    
    video.addEventListener('ended', () => {
        playPauseBtn.textContent = 'Replay';
    });
});
