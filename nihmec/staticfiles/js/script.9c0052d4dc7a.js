
function displayNextSibling(ele) {
    ele.nextElementSibling.classList.toggle('display-none');
    // document.querySelector(`.${ele.nextElementSibling.classList[0]} svg`).style.transform = 'rotate(-180deg)';
}

function displaySideMenu() {
    document.querySelector('.ham-side-nav-bar').classList.toggle('translate-left-right');
}

let navbarhead = document.querySelector('.nav-head-container');
let navbar = document.querySelector('.navigation-menu');

let sticky = navbarhead.offsetTop;

// function fixNavOnScroll(){
//     if(window.pageXOffset >= sticky){
//         navbar.classList.add("sticky");
//         navbarhead.style.display = 'none';
//     }else{
//         navbar.classList.remove("sticky");
//     }
// }

// document.addEventListener('scroll', fixNavOnScroll, false);

let imp_page = document.querySelector('.imp-page');

function displayImpPages() {
    imp_page.classList.toggle('display-none');
}

let Img = document.querySelectorAll('img');

Img.forEach(img => {
    img.setAttribute("loading", "lazy");
});