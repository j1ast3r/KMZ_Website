const seatMap = document.querySelector('map[name="seat-map-map"]');
const selectedSeats = document.querySelector('.selected-seats');
const totalPrice = document.querySelector('.total-price');
const bookBtn = document.querySelector('.book-btn');
const buyBtn = document.querySelector('.buy-btn');

let selectedSeatsArray = [];
let totalPriceValue = 0;

// Функция для обработки клика по месту на схеме
function handleSeatClick(event) {
    const seat = event.target.closest('area');
    if (!seat) return;

    const seatName = seat.alt;
    const seatPrice = parseFloat(seat.dataset.price);

    if (selectedSeatsArray.includes(seatName)) {
        // Если место уже выбрано, убрать его из списка
        selectedSeatsArray = selectedSeatsArray.filter(item => item !== seatName);
        totalPriceValue -= seatPrice;
    } else {
        // Если место не выбрано, добавить его в список
        selectedSeatsArray.push(seatName);
        totalPriceValue += seatPrice;
    }

    renderSelectedSeats();
    updateTotalPrice();
}

// Функция для отображения выбранных мест в корзине
function renderSelectedSeats() {
    selectedSeats.innerHTML = '';
    selectedSeatsArray.forEach(seat => {
        const li = document.createElement('li');
        li.textContent = seat;
        selectedSeats.appendChild(li);
    });
}

// Функция для обновления общей стоимости
function updateTotalPrice() {
    totalPrice.textContent = `${totalPriceValue.toFixed(2)} руб.`;
}

// Обработчик события клика по кнопке "Забронировать"
bookBtn.addEventListener('click', () => {
    if (selectedSeatsArray.length === 0) {
        alert('Пожалуйста, выберите места для бронирования.');
    } else {
        // Здесь можно добавить логику для отправки данных на сервер
        alert(`Вы забронировали следующие места: ${selectedSeatsArray.join(', ')}`);
    }
});

// Обработчик события клика по кнопке "Купить"
buyBtn.addEventListener('click', () => {
    if (selectedSeatsArray.length === 0) {
        alert('Пожалуйста, выберите места для покупки.');
    } else {
        // Здесь можно добавить логику для оплаты и покупки билетов
        alert(`Вы купили следующие места: ${selectedSeatsArray.join(', ')}. Общая стоимость: ${totalPriceValue.toFixed(2)} руб.`);
    }
});

// Добавление обработчика события клика по местам на схеме
seatMap.addEventListener('click', handleSeatClick);