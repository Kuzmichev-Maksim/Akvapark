document.addEventListener('DOMContentLoaded', function () {
    // Инициализация переменных
    let adultPrice = 0;
    const serviceSelect = document.getElementById('service');
    const totalPriceElement = document.getElementById('totalPrice');
    const adultPriceElement = document.querySelectorAll('.visitor-type .price')[0];
    const dateInput = document.getElementById('date');
    const paymentModal = document.getElementById('paymentModal');
    const closeModal = document.getElementById('closeModal');
    const paymentForm = document.getElementById('paymentForm');
    const buyButton = document.getElementById('buyButton');

    // Получаем скрытое поле для даты посещения
    const visitDateInput = document.getElementById('visitDate');

    // Установка сегодняшней даты
    setTodayDate();

    // Функция для установки сегодняшней даты в формате YYYY-MM-DD
    function setTodayDate() {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${yyyy}-${mm}-${dd}`;
        visitDateInput.value = dateInput.value; // Устанавливаем начальное значение скрытого поля
    }

    // Обработчик изменения даты
    dateInput.addEventListener('change', function () {
        visitDateInput.value = dateInput.value; // Обновляем значение скрытого поля
    });

    // Функция для обновления общей суммы
    function updateTotalPrice() {
        const adultQuantity = parseInt(document.querySelectorAll('.visitor-type .quantity')[0].textContent) || 0;
        const childQuantity = parseInt(document.querySelectorAll('.visitor-type .quantity')[1].textContent) || 0;
        const babyQuantity = parseInt(document.querySelectorAll('.visitor-type .quantity')[2].textContent) || 0;

        const childPrice = 1500;
        const babyPrice = 500;

        const totalPrice = (adultQuantity * adultPrice) + (childQuantity * childPrice) + (babyQuantity * babyPrice);
        totalPriceElement.textContent = totalPrice + " РУБ.";

        // Обновление скрытых полей формы
        document.getElementById('totalAmount').value = totalPrice;
        document.getElementById('adultQuantity').value = adultQuantity;
        document.getElementById('childQuantity').value = childQuantity;
        document.getElementById('babyQuantity').value = babyQuantity;
        document.getElementById('serviceId').value = serviceSelect.value; // Сохраняем выбранную услугу
    }

    // Обработчик изменения услуги
    serviceSelect.addEventListener('change', function () {
        const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
        adultPrice = parseFloat(selectedOption.dataset.price) || 0;
        adultPriceElement.textContent = adultPrice + " руб.";
        updateTotalPrice();
    });

    // Обработчик изменения количества посетителей
    document.querySelectorAll('.visitor-type').forEach((visitorType, index) => {
        const quantityElement = visitorType.querySelector('.quantity');
        const plusButton = visitorType.querySelector('.plus');
        const minusButton = visitorType.querySelector('.minus');

        // Увеличение количества
        plusButton.addEventListener('click', function () {
            let currentQuantity = parseInt(quantityElement.textContent) || 0;
            quantityElement.textContent = currentQuantity + 1;
            updateTotalPrice();
        });

        // Уменьшение количества
        minusButton.addEventListener('click', function () {
            let currentQuantity = parseInt(quantityElement.textContent) || 0;
            if (currentQuantity > 0) {
                quantityElement.textContent = currentQuantity - 1;
                updateTotalPrice();
            }
        });
    });

    // Установка цены для взрослого посетителя по умолчанию, если такая услуга выбрана
    if (serviceSelect.options.length > 0) {
        const selectedOption = serviceSelect.options[0];
        adultPrice = parseFloat(selectedOption.dataset.price) || 0;
        adultPriceElement.textContent = adultPrice + " руб.";
    }

    // Открытие модального окна при нажатии на кнопку "Купить"
    buyButton.addEventListener('click', function () {
        paymentModal.style.display = "block"; // Отображение модального окна
        setTimeout(function () {
            paymentModal.style.opacity = "1"; // Плавное появление
            paymentModal.querySelector('.modal-content').style.transform = "translateY(0)"; // Плавный подъём окна
        }, 10);
    });

    // Закрытие модального окна
    closeModal.addEventListener('click', function () {
        paymentModal.style.opacity = "0"; // Плавное исчезновение
        paymentModal.querySelector('.modal-content').style.transform = "translateY(-50px)"; // Сдвиг окна вверх
        setTimeout(function () {
            paymentModal.style.display = "none"; // Скрытие окна после анимации
        }, 300); // Время, соответствующее продолжительности анимации
    });

    paymentForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Получаем данные из формы
        const cardNumber = document.getElementById('cardNumber').value;
        const expiryDate = document.getElementById('expiryDate').value;
        const cvv = document.getElementById('cvv').value;
        const cardholderName = document.getElementById('cardholderName').value;

        // Простая валидация
        const cardNumberRegex = /^\d{16}$/;
        const expiryDateRegex = /^(0[1-9]|1[0-2])\/?([0-9]{2})$/;
        const cvvRegex = /^\d{3}$/;

        if (!cardNumberRegex.test(cardNumber)) {
            alert('Неверный номер карты');
            return;
        }

        if (!expiryDateRegex.test(expiryDate)) {
            alert('Неверная дата окончания');
            return;
        }

        if (!cvvRegex.test(cvv)) {
            alert('Неверный CVV');
            return;
        }

        if (!cardholderName) {
            alert('Введите имя владельца');
            return;
        }

        // Отправка данных на сервер
        fetch('/process-payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams(new FormData(paymentForm)).toString()
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                    paymentModal.style.display = "none"; // Скрытие модального окна после успешной оплаты
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при обработке оплаты');
            });
    });

    //Добавляем обработчик на поле с датой
    document.getElementById('expiryDate').addEventListener('input', function (e) {
        let input = e.target.value;

        // Удаляем все нецифровые символы
        input = input.replace(/\D/g, '');

        // Форматируем строку как MM/YY
        if (input.length > 2) {
            input = input.substring(0, 2) + '/' + input.substring(2, 4);
        }

        // Ограничиваем ввод до 5 символов (2 цифры, слеш, 2 цифры)
        if (input.length > 5) {
            input = input.substring(0, 5);
        }

        e.target.value = input;
    });
});
