const infoMenu = document.getElementsByClassName("infoMenu");
const studentForm = document.getElementsByClassName("student-form");

document.getElementById("addinfo").addEventListener('click', () => {
    console.log("button clicked");
    infoMenu.style.hidden = true;
    studentForm.style.hidden = false;
});

const navSlide = () => {
    
    const burger      = document.querySelector('.burger');
    const nav         = document.querySelector('.nav-links');
    const navLinks    = document.querySelectorAll('.nav-links li');
    
    //toggle navbar
    burger.addEventListener('click', () => {
        nav.classList.toggle('nav-active');
         //animate links in navbar
        navLinks.forEach((link, index) => {
            //console.log(index);
            if (link.style.animation){
                link.style.animation = '';
            }else{
                link.style.animation = `navLinksFade 0.5s ease forwards ${index / 7 + 0.3 }s`;
            }
        });
        //console.log("en");
        burger.classList.toggle('toggle');
        //console.log("done");
    });
}

navSlide();


