document.addEventListener('DOMContentLoaded', () => {
    const player = new Plyr('#player', {
        keyboard: { focused: true, global: true },
        tooltips: { controls: true, seek: true },
        captions: { active: true, update: true, language: 'auto' },
        quality: { default: 1080, options: [1080, 720, 480] }
    });

    // Save Progress
    const videoId = window.location.pathname.split('/').pop();
    const savedTime = localStorage.getItem(`watch_progress_${videoId}`);

    if (savedTime) {
        player.once('ready', () => {
            player.currentTime = parseFloat(savedTime);
        });
    }

    player.on('timeupdate', () => {
        if (player.currentTime > 0) {
            localStorage.setItem(`watch_progress_${videoId}`, player.currentTime);
        }
    });

    // Auto Next Episode (Mock logic as we don't have full library access here yet)
    player.on('ended', () => {
        console.log('Video ended. Loading next episode...');
        const nextBtn = document.getElementById('next-ep');
        if (nextBtn) {
            nextBtn.click();
        }
    });

    // Track selection handling
    const audioSelector = document.getElementById('audio-selector');
    const subtitleSelector = document.getElementById('subtitle-selector');

    audioSelector.addEventListener('change', (e) => {
        console.log(`Switching audio to track ${e.target.value}`);
        // In a real OTT system, this might reload the stream with a specific track filter
        // or switch tracks in an HLS/Dash stream.
        // For basic MP4/MKV, it's limited unless we re-mux on the fly.
    });

    subtitleSelector.addEventListener('change', (e) => {
        console.log(`Switching subtitles to ${e.target.value}`);
        // Subtitle logic
    });

    // Expose player for debugging or advanced controls
    window.player = player;
});
