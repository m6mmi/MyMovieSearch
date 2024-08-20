document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('#slideshow .slide');
    let currentSlide = 0;

    if (slides.length === 0) {
        console.error('No slides found.');
        return;
    }

    function showNextSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
    }

    slides[currentSlide].classList.add('active');
    setInterval(showNextSlide, 3000);
});
