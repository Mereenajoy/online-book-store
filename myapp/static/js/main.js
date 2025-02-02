const searchButton = document.getElementById('search-button'),
searchClose = document.getElementById('search__close'),
searchContent = document.getElementById('search-content')

if(searchButton){
    searchButton.addEventListener('click',()=>{
        searchContent.classList.add('show-search')
    })
}

if(searchClose){
    searchClose.addEventListener('click',()=>{
        searchContent.classList.remove('show-search')
    })
}


/*====================ADD SHADOW HEADER=============================*/

const shadowHeader =()=>{
    const header =document.getElementById('header')
    this.scrollY >=50 ? header.classList.add('shadow-header')
                      : header.classList.remove('shadow-header')
}
window.addEventListener('scroll',shadowHeader)




/* home swiper */

let swiperHome = new Swiper('.home__swiper', {
    loop:true,
    spaceBetween: -24,
    grabCursor:true,
    slidesPerView:'auto',
    centeredSlides:'auto',

    autoplay:{
        delay:3000,
        disableOnInteraction:false,
    },
    breakpoints:{
        1220:{
            spaceBetween:-32,
        }
    }
})


const scrollUp =()=>{
    const scrollUp = document.getElementById('scroll-up')
    this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
                        : scrollUp.classList.remove('show-scroll')
}

window.addEventListener('scroll',scrollUp)


const section =document.querySelectorAll('section[id')

const scrollActive =()=>{
    const scrollDown = window.scrollY

  section.forEach(current =>{
    const sectionHeight = current.offsetHeight,
        sectionTop = current.offsetTop - 58,
        sectionId = current.getAttribute('id')
        sectionClass = document.querySelector('.nav__menu a[href*=' + sectionId + ']')

    if(scrollDown > sectionTop && scrollDown <= sectionTop + sectionHeight){
        sectionClass.classList.add('active-link')
     }
     else{
        sectionClass.classList.remove('active-link')
     }
  })
}
window.addEventListener('scroll',scrollActive)



const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme ='ri-sun-line'

const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

const getCurrentTheme = ()=> document.body.classList(darkTheme) ? 'dark': 'light'
const getCurrentIcon =()=> document.classList.contains(iconTheme) ? 'ri-moon-line' : 'ri-sun-line'

if(selectedTheme){
    document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
    themeButton.classList[selectedIcon === 'ri-moon-line' ? 'add' : 'remove'](iconTheme)
}

themeButton.addEventListener('click',()=>{
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    localStorage.setItem('selected-theme',getCurrentTheme())
    localStorage.setItem('selected-icon',getCurrentIcon())
})

const sr = scrollReveal({
    origin:'top',
    distance:'60px',
    duration:2500,
    delay:400,
    // reset:true ,
})

sr.reveal(`.home__data`)
sr.reveal(`.home__images`,{delay:600})
sr.reveal(`.services__card`,{interval:100})