// Код для липкой шапки
window.onscroll = function() {
    var headerTop = document.querySelector('.header-top');
    if (window.pageYOffset > 0) {
        headerTop.classList.add('sticky');
    } else {
        headerTop.classList.remove('sticky');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const seatingChart = document.getElementById('seating-chart');
    const selectedSeatsList = document.getElementById('selected-seats-list');
    let selectedSeats = [];

    // Предполагаем, что функция renderSeats из buttons.js создает кнопки сидений
    if (typeof renderSeats === 'function') {
        renderSeats(seatingChart);
    }

    // Добавляем обработчик событий для кликов по сиденьям
    seatingChart.addEventListener('click', function(event) {
        if (event.target.classList.contains('seat-button')) {
            const seatId = event.target.dataset.seatId;
            const row = event.target.dataset.row;
            const number = event.target.dataset.number;

            if (selectedSeats.some(seat => seat.id === seatId)) {
                // Если место уже выбрано, удаляем его
                selectedSeats = selectedSeats.filter(seat => seat.id !== seatId);
            } else {
                // Добавляем новое выбранное место
                selectedSeats.push({ id: seatId, row, number });
            }

            updateSelectedSeatsList();
        }
    });

    function updateSelectedSeatsList() {
        selectedSeatsList.innerHTML = '';
        selectedSeats.forEach(seat => {
            const seatItem = document.createElement('div');
            seatItem.classList.add('seat-item');
            seatItem.innerHTML = `
                <span>Sitzplatz: Reihe ${seat.row}, Platz ${seat.number}</span>
                <button class="remove-seat" data-seat-id="${seat.id}">×</button>
            `;
            selectedSeatsList.appendChild(seatItem);
        });

        // Обновляем текст кнопки оформления заказа
        const checkoutButton = document.querySelector('.checkout-button');
        checkoutButton.textContent = `${selectedSeats.length} Ticket für € ${(selectedSeats.length * 96.99).toFixed(2)}`;
    }

    // Обработчик для удаления выбранных мест
    selectedSeatsList.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-seat')) {
            const seatId = event.target.dataset.seatId;
            selectedSeats = selectedSeats.filter(seat => seat.id !== seatId);
            updateSelectedSeatsList();
        }
    });
});