document.addEventListener('DOMContentLoaded', function () {
    const plusButtons = document.querySelectorAll('.plus');
    const minusButtons = document.querySelectorAll('.minus');
    const quantityDisplays = document.querySelectorAll('.quantity');

    // Увеличение количества
    plusButtons.forEach(button => {
        button.addEventListener('click', function () {
            const quantityDisplay = this.previousElementSibling;
            const currentQuantity = parseInt(quantityDisplay.textContent) || 0;
            quantityDisplay.textContent = currentQuantity + 1;
            updateTotalPrice();
        });
    });

    // Уменьшение количества
    minusButtons.forEach(button => {
        button.addEventListener('click', function () {
            const quantityDisplay = this.nextElementSibling;
            const currentQuantity = parseInt(quantityDisplay.textContent) || 0;
            if (currentQuantity > 0) {
                quantityDisplay.textContent = currentQuantity - 1;
            }
            updateTotalPrice();
        });
    });

    // Функция для пересчета итоговой цены
    function updateTotalPrice() {
        const adultQuantity = parseInt(document.querySelectorAll('.visitor-type .quantity')[0].textContent) || 0;
        const childQuantity = parseInt(document.querySelectorAll('.visitor-type .quantity')[1].textContent) || 0;
        const babyQuantity = parseInt(document.querySelectorAll('.visitor-type .quantity')[2].textContent) || 0;

        const adultPrice = 2800; // Цена взрослого
        const childPrice = 1500; // Цена ребенка
        const babyPrice = 500;  // Цена малыша

        const totalPrice = (adultQuantity * adultPrice) + (childQuantity * childPrice) + (babyQuantity * babyPrice);
        document.getElementById('totalPrice').textContent = totalPrice + " руб.";
    }
});



document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('date');
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
});
