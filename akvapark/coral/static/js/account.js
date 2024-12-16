document.addEventListener('DOMContentLoaded', function () {
    const starRating = document.getElementById('star-rating');
    const stars = starRating.querySelectorAll('label');

    stars.forEach((star, index) => {
        // Обработчик наведения
        star.addEventListener('mouseover', function () {
            stars.forEach((s, i) => {
                // Закрашиваем все звезды до текущей
                if (i <= index) {
                    s.classList.add('hovered');
                } else {
                    s.classList.remove('hovered');
                }
            });
        });

        // Убираем эффект наведения
        star.addEventListener('mouseout', function () {
            stars.forEach(s => s.classList.remove('hovered'));
        });

        // Обработчик клика (выбор рейтинга)
        star.addEventListener('click', function () {
            // Убираем класс checked со всех звезд
            stars.forEach(s => s.classList.remove('checked'));

            // Добавляем класс checked к текущей звезде и всем предыдущим
            for (let i = 0; i <= index; i++) {
                stars[i].classList.add('checked');
            }
        });
    });
});
