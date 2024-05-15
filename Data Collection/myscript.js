
(function() {
    'use strict';

    function clickElement(selector) {
        let element = document.querySelector(selector);
        if (element) {
            element.click();
        } else {
            console.error("Element not found:", selector);
        }
    }

    function parseTable(table, dataArray) {
        let rows = table.querySelectorAll('.style_order__book__row__container__5ukyU');
        rows.forEach(row => {
            let price = row.querySelector('.style_order__book__table__left__147jG').textContent.trim();
            let quantity = row.querySelector('.style_order__book__table__right__1FcjI').textContent.trim();
            dataArray.push({ price: parseFloat(price), quantity: parseInt(quantity) });
        });
    }

    function formatTime(date) {
        const options = {
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
            hour12: false
        };
        return date.toLocaleString('en-US', options);
    }
    const socket = io('http://localhost:5000');
    function sendDataToServer(yesData, noData, title,currentTime) {
        socket.emit('order_book_data', { 
            yesData, 
            noData, 
            title,
            currentTime
        });
    }

    function convertStringToTime(timeString) {
        const [time, period] = timeString.split(' ');
        const [hours, minutes] = time.split('-').map(Number);

        let hours24 = hours;
        if (period === 'PM' && hours !== 12) {
            hours24 = hours + 12;
        } else if (period === 'AM' && hours === 12) {
            hours24 = 0;
        }

        const date = new Date();
        date.setHours(hours24);
        date.setMinutes(minutes);
        date.setSeconds(0);

        return date;
    }

    function handleOrderBook() {
        let h = document.getElementsByClassName('style_order__book__2Dxmj')[0];

        if (h) {
            let yesData = [];
            let noData = [];

            let yesTable = h.querySelectorAll('.style_order__book__table__2zTLv')[0];
            parseTable(yesTable, yesData);

            let noTable = h.querySelectorAll('.style_order__book__table__2zTLv')[1];
            parseTable(noTable, noData);

            var title = document.querySelector('.style_bottom__sheet__event__name__2hoEf');
            title = title.textContent || title.innerText
            title = title.slice(-9).slice(0,8).replace(/:/g,'-')

            var timeOfQuestion = convertStringToTime(title)
            var currentTime = new Date();

            if (timeOfQuestion > currentTime) {
                sendDataToServer(yesData, noData, title,currentTime)
            } else {
                location.reload()
            }

        } else {
            console.error("Order book element not found.");
        }
    }

    setTimeout(function() {
        clickElement(".style_arena__filter__item__3VlSl:nth-child(4)");

        setTimeout(function() {
            clickElement('.style_event__card__actions__button__107m2.style_event__card__actions__button__yes__2V1x2');

            setTimeout(function() {
                clickElement('.style_order__book__top__3keFx');
                setInterval(handleOrderBook, 200)
            }, 1000);
        }, 1500);
    }, 3000);
})();

