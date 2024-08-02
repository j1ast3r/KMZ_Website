document.addEventListener('DOMContentLoaded', function() {
    const seatingChart = document.getElementById('seating-chart');
    const selectedSeatsList = document.getElementById('selected-seats-list');
    const totalPriceElement = document.querySelector('.total-price');
    const reserveBtn = document.getElementById('reserve-button');
    const buyBtn = document.getElementById('buy-button');

    if (!seatingChart || !selectedSeatsList || !totalPriceElement || !reserveBtn || !buyBtn) {
        console.error('Не найдены необходимые элементы DOM');
        return;
    }

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.setAttribute("viewBox", "0 -3 872 780");
    seatingChart.appendChild(svg);

    const seatsGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    svg.appendChild(seatsGroup);

    let selectedSeats = new Set();
    let totalPrice = 0;
    const ticketPrice = 10; // Цена билета

    const rowSeats = {
    1: 8, 2: 16, 3: 16, 4: 16, 5: 16, 6: 16,
    7: 18, 8: 18, 9: 18, 10: 18, 11: 18, 12: 18, 13: 18, 14: 18,
    15: 22, 16: 22, 17: 22, 18: 22, 19: 22, 20: 22, 21: 22, 22: 22, 23: 22,
    24: 26, 25: 26, 26: 22, 27: 18, 28: 14, 29: 12, 30: 14, 31: 26, 32: 24, 33: 18
};

function createSeat(pathData, index) {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathData.d);
    path.setAttribute("fill", pathData.fill);

    let currentRow = 1;
    let currentSeat = 0;
    let totalSeats = 0;

    for (let row in rowSeats) {
        if (totalSeats + rowSeats[row] > index) {
            currentRow = parseInt(row);
            currentSeat = index - totalSeats + 1;
            break;
        }
        totalSeats += rowSeats[row];
    }

    path.setAttribute("data-seat-number", index + 1);
    path.setAttribute("data-row", currentRow);
    path.setAttribute("data-seat", currentSeat);
    seatsGroup.appendChild(path);

    path.addEventListener('click', function() {
        toggleSeat(this, index + 1, currentRow, currentSeat);
    });
}

    function toggleSeat(path, seatNumber) {
        if (path.getAttribute("fill") === "#05FF00") {
            path.setAttribute("fill", "#FFA500");
            selectedSeats.add(seatNumber);
            addSelectedSeat(seatNumber);
        } else if (path.getAttribute("fill") === "#FFA500") {
            path.setAttribute("fill", "#05FF00");
            selectedSeats.delete(seatNumber);
            removeSelectedSeat(seatNumber);
        }
        updateTotalPrice();
    }

    function addSelectedSeat(seatNumber) {
        const seatItem = document.createElement('div');
        seatItem.classList.add('seat-item');
        seatItem.innerHTML = `
            Место ${seatNumber}
            <span class="remove-seat" data-seat-number="${seatNumber}">×</span>
        `;
        selectedSeatsList.appendChild(seatItem);
        totalPrice += ticketPrice;
    }

    function removeSelectedSeat(seatNumber) {
        const seatItem = selectedSeatsList.querySelector(`.seat-item [data-seat-number="${seatNumber}"]`).parentNode;
        if (seatItem) {
            seatItem.remove();
        }
        totalPrice -= ticketPrice;
    }

    function updateTotalPrice() {
        totalPriceElement.textContent = `Общая стоимость: €${totalPrice.toFixed(2)}`;
    }

    selectedSeatsList.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-seat')) {
            const seatNumber = parseInt(event.target.dataset.seatNumber);
            removeSelectedSeat(seatNumber);
            const seatPath = seatsGroup.querySelector(`[data-seat-number="${seatNumber}"]`);
            if (seatPath) {
                seatPath.setAttribute("fill", "#05FF00");
            }
            selectedSeats.delete(seatNumber);
            updateTotalPrice();
        }
    });

    reserveBtn.addEventListener('click', () => addToCart('reserve'));
    buyBtn.addEventListener('click', () => addToCart('buy'));

    function addToCart(action) {
    if (selectedSeats.size === 0) {
        alert('Пожалуйста, выберите места');
        return;
    }

    const csrftoken = getCookie('csrftoken');
    const eventId = document.querySelector('meta[name="event-id"]').getAttribute('content');
    const seatsArray = Array.from(selectedSeats).map(seatNumber => {
        const seatElement = seatsGroup.querySelector(`[data-seat-number="${seatNumber}"]`);
        return {
            number: seatNumber,
            row: seatElement.getAttribute('data-row'),
            seat: seatElement.getAttribute('data-seat')
        };
    });

    console.log('Отправка данных на сервер:', {
        seats: seatsArray,
        action: action,
        event_id: eventId
    });

    fetch('/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            seats: seatsArray,
            action: action,
            event_id: eventId
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(data => {
        console.log('Ответ сервера:', data);
        if (data.success) {
            alert(action === 'reserve' ? 'Места зарезервированы' : 'Билеты добавлены в корзину');
            window.location.href = '/cart/';
        } else {
            throw new Error(data.error || 'Неизвестная ошибка');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при обработке запроса: ' + (error.error || error.message));
    });
}

    // Создаем места
    svgPaths.forEach(createSeat);

    // Функция для получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});