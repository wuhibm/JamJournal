
document.addEventListener('DOMContentLoaded', () => {

    let navItems = document.querySelectorAll(".nav-item");
    console.log(navItems)
    //reset_nav(navItems);

    navItems.forEach(navitem => {
        navitem.addEventListener('click', () => {
            console.log(navitem);
            reset_nav(navItems);
            navitem.classList.add("active");
            console.log(navitem);
        });
    });
    console.log(navItems)
});

function reset_nav(navItems) {
    navItems.forEach(navitem => { navitem.classList.remove("active") });
}