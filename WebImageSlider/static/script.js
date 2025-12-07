document.addEventListener('DOMContentLoaded', () => {

    // --- IMPORTANT ---
    // 1. Add your image files to the 'static/images' folder.
    // 2. Replace the placeholder names in this list with your actual file names.
    const images = [
        "image1.jpg",
        "image2.png",
        "image3.gif",
        // Add more image file names here
    ];

    const slide = document.getElementById('slide');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const playPauseBtn = document.getElementById('play-pause-btn');

    let currentIndex = 0;
    let intervalId = null;

    function showImage(index) {
        // Check if the images array is empty
        if (images.length === 0) {
            slide.alt = "No images found. Please add images to the static/images folder and update script.js.";
            return;
        }
        const imagePath = `static/images/${images[index]}`;
        slide.src = imagePath;
        slide.alt = images[index];
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        showImage(currentIndex);
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage(currentIndex);
    }

    function playSlideshow() {
        if (intervalId === null) {
            intervalId = setInterval(nextImage, 3000); // 3-second interval
            playPauseBtn.textContent = 'Pause';
        }
    }

    function pauseSlideshow() {
        if (intervalId !== null) {
            clearInterval(intervalId);
            intervalId = null;
            playPauseBtn.textContent = 'Play';
        }
    }

    function togglePlayPause() {
        if (intervalId === null) {
            playSlideshow();
        } else {
            pauseSlideshow();
        }
    }

    // Event Listeners
    nextBtn.addEventListener('click', () => {
        pauseSlideshow();
        nextImage();
    });

    prevBtn.addEventListener('click', () => {
        pauseSlideshow();
        prevImage();
    });

    playPauseBtn.addEventListener('click', togglePlayPause);

    // Initial image load
    showImage(currentIndex);
});
