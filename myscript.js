// ==UserScript==
// @name         IPL
// @namespace    http://localhost:5000/
// @version      0.1
// @description  IPL
// @author       Sindhav Khushal
// @match        https://trading.probo.in/arena
// @grant        GM_xmlhttpRequest
// ==/UserScript==
(function() {
    'use strict';

    function dragSlider(className, newValue) {
    var sliderButton = document.querySelector('.' + className + ' .style_rsbcSliderCircle__2Vh-4'); // Select slider button by class
    var slider = sliderButton.parentElement; // Get parent element of slider button
    var sliderRect = slider.getBoundingClientRect();

    var sliderButtonRect = sliderButton.getBoundingClientRect();
    var sliderButtonOffset = sliderButtonRect.left - sliderRect.left; // Calculate offset of slider button within slider

    var endX = sliderRect.left + (sliderRect.width * parseFloat(newValue) / 100) - sliderButtonOffset;

    var mouseDownEvent = new MouseEvent('mousedown');
    var mouseMoveEvent = new MouseEvent('mousemove');
    var mouseUpEvent = new MouseEvent('mouseup');

    sliderButton.dispatchEvent(mouseDownEvent);
    sliderButton.dispatchEvent(mouseMoveEvent);
    sliderButton.dispatchEvent(new MouseEvent('mousemove', { clientX: endX }));
    sliderButton.dispatchEvent(mouseUpEvent);
    }

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

// ==UserScript==
// @name         Send Data to Server
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Send data to the server
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==
    function sendDataToServer(yesData, noData, title) {
        // Define the data you want to send
        var data = {
            yesData: yesData,
            noData: noData,
            title: title
        };

        var jsonData = JSON.stringify(data);
        var serverUrl = 'http://localhost:5000';

        fetch(serverUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data sent successfully:', data);
        })
        .catch(error => {
            console.error('Error sending data:', error);
        });
    }

    function convertStringToTime(timeString) {
        // Split the string into hours, minutes, and AM/PM
        const [time, period] = timeString.split(' ');
        const [hours, minutes] = time.split('-').map(Number);

        // Convert hours to 24-hour format if PM
        let hours24 = hours;
        if (period === 'PM' && hours !== 12) {
            hours24 = hours + 12;
        } else if (period === 'AM' && hours === 12) {
            // Convert 12 AM to 24-hour format (midnight)
            hours24 = 0;
        }

        // Create a new Date object with the given hours and minutes
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
                sendDataToServer(yesData, noData, title)
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
                setInterval(handleOrderBook, 500)
            }, 1000);
        }, 1500);
    }, 3000);
})();

