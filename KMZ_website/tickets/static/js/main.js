// Код для липкой шапки
window.onscroll = function() {
    var headerTop = document.querySelector('.header-top');
    if (window.pageYOffset > 0) {
        headerTop.classList.add('sticky');
    } else {
        headerTop.classList.remove('sticky');
    }
}



