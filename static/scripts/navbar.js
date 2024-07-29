
document.getElementById('toggle-nav').addEventListener('click', ()=>{
    let menu = document.getElementById('mobile-nav');
    console.log("Click")
    if (menu.style.display === 'flex') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'flex';
    }
});