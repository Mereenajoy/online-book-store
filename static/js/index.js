let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick =()=>{
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('open');
};

window.onscroll =()=>{
    menu.classList.remove('bx-x');
    navbar.classList.remove('open')
};

const sr = ScrollReveal({
    distance : '60px',
    duration : 2500,
    delay : 400,
    reset : true
})

sr.reveal('.home-text',{delay:200 , origin:'top'});
sr.reveal('.home-img',{delay:300 , origin:'top'});
sr.reveal('.product ,.cta-content , .contact ',{delay:200 , origin:'top'});