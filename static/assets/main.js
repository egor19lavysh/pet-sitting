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

  let inputs = document.querySelectorAll('.input__file');
    Array.prototype.forEach.call(inputs, function (input) {
      let label = input.nextElementSibling,
        labelVal = label.querySelector('.input__file-button-text').innerText;
  
      input.addEventListener('change', function (e) {
        let countFiles = '';
        if (this.files && this.files.length >= 1)
          countFiles = this.files.length;
  
        if (countFiles)
          label.querySelector('.input__file-button-text').innerText = 'Выбрано файлов: ' + countFiles;
        else
          label.querySelector('.input__file-button-text').innerText = labelVal;
      });
    });