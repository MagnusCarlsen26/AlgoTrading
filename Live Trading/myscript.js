(function() {
    'use strict';

    function clickElement(selector,index) {
        let element = document.querySelectorAll(selector)[index];
        if (element) {
            element.click();
        } else {
            console.error("Element not found:", selector);
        }
    }


    function slideSlider(target) {
        socket.emit('order_book_data',{
            message : "Question Opened"
        })
        console.log('///')
    }
    
    var scriptElement = document.createElement('script');
    scriptElement.src = "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.0/socket.io.min.js";
    document.head.appendChild(scriptElement);
    var socket

    console.log('sdfv')
    setTimeout(function() {
        clickElement('.style_card_container__3-ZxN',0);
        setTimeout(function() {
            clickElement('.style_trade__info__header__right__button__25KfD',0);
            socket = io('http://localhost:6000');
            setTimeout(function() {
                clickElement('.style_bottom__sheet__footer__container__exit__RJugJ',0)
                setTimeout(function () {
                    slideSlider(8)
                },1000)
            }, 1000);
        }, 1500);
    }, 1000);
})();
