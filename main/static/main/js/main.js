var menuButton = document.querySelector('.burger');
var menu = document.querySelector('.nav_bar');
menuButton.addEventListener('click', function () {
    menuButton.classList.toggle('burger-active');
    menu.classList.toggle('nav_bar_active');
})

const tabs = document.querySelectorAll('.plus');
    
tabs.forEach(tab => {
    tab.addEventListener('click', () =>{
        const targetId = tab.getAttribute('data-target');
        const targetTable = document.getElementById(targetId);
        targetTable.classList.toggle('txt_tab');
        targetTable.classList.toggle('txt_tab_active');
    });
});

var swiper = new Swiper(".mySwiper", {
    spaceBetween: 30,
    centeredSlides: true,
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });