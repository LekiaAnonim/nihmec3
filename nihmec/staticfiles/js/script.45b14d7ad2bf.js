
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


let imp_page = document.querySelector('.imp-page');

function displayImpPages() {
    imp_page.classList.toggle('display-none');
}

let Img = document.querySelectorAll('img');

Img.forEach(img => {
    img.setAttribute("loading", "lazy");
});

// Payment option selection
let paymentOption = document.querySelectorAll("input[name='currency']");
let nairaPayment = document.querySelector(".naira-payment");
let dollarPayment = document.querySelector(".dollar-payment");
function togglePaymentOption(ele) {
    if (ele.id == 'id_currency_0'){
        nairaPayment.classList.remove('display-none');
        dollarPayment.classList.add('display-none');
        console.log(ele.id);
    }else{
        nairaPayment.classList.add('display-none');
        dollarPayment.classList.remove('display-none');
        console.log(ele.id);
    }
}

paymentOption.forEach((ele)=>{
    ele.setAttribute('onclick', 'togglePaymentOption(this)');
})