document.addEventListener('DOMContentLoaded', () => {
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');

    let currentIndex = 0;

    // Копируем первый и последний слайды для эффекта бесконечности
    const firstSlide = slides[0].cloneNode(true);
    const lastSlide = slides[slides.length - 1].cloneNode(true);

    slider.appendChild(firstSlide);
    slider.insertBefore(lastSlide, slides[0]);

    const slideWidth = slides[0].clientWidth;

    // Устанавливаем начальную позицию слайдера
    slider.style.transform = `translateX(-${slideWidth}px)`;

    // Функция обновления слайдера
    const updateSlider = () => {
        slider.style.transform = `translateX(-${(currentIndex + 1) * slideWidth}px)`;
    };

    // Переход к следующему слайду
    const nextSlide = () => {
        currentIndex++;
        slider.style.transition = 'transform 0.5s ease-in-out';
        updateSlider();

        // Возврат к первому слайду
        slider.addEventListener('transitionend', () => {
            if (currentIndex === slides.length) {
                slider.style.transition = 'none';
                currentIndex = 0;
                updateSlider();
            }
        });
    };

    // Переход к предыдущему слайду
    const prevSlide = () => {
        currentIndex--;
        slider.style.transition = 'transform 0.5s ease-in-out';
        updateSlider();

        // Возврат к последнему слайду
        slider.addEventListener('transitionend', () => {
            if (currentIndex < 0) {
                slider.style.transition = 'none';
                currentIndex = slides.length - 1;
                updateSlider();
            }
        });
    };

    // События для кнопок
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);

    // Автоматическая прокрутка
    setInterval(nextSlide, 5000); // Прокрутка каждые 5 секунд
});
