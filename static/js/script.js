
function displayNextSibling(ele) {
    ele.nextElementSibling.classList.toggle('display-none');
    // document.querySelector(`.${ele.nextElementSibling.classList[0]} svg`).style.transform = 'rotate(-180deg)';
}

function displaySideMenu() {
    document.querySelector('.ham-side-nav-bar').classList.toggle('translate-left-right');
}

