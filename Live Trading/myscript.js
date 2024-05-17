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

    function sendDataToServer(yesData, noData, title,currentTime) {
        socket.emit('order_book_data', { 
            yesData, 
            noData, 
            title,
            currentTime
        });
    }

    function Slide(price) {
        
    }

    var scriptElement = document.createElement('script');
    scriptElement.src = "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.0/socket.io.min.js";
    document.head.appendChild(scriptElement);
    var socket

    setTimeout(function() {  
        clickElement('.style_card_container__3-ZxN');
        setTimeout(function() {
            clickElement('.style_trade__info__header__right__button__25KfD');
            socket = io('http://localhost:5000');
            setTimeout(function() {
                clickElement('.style_bottom__sheet__footer__container__exit__RJugJ')
                setInterval(Slide, 200)
            }, 1000);
        }, 1500);
    }, 3000);
})();

