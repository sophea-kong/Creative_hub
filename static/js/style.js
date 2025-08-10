function scrollDownAbout(){
    document.getElementById('about-me-id1').scrollIntoView({ behavior: 'smooth', block: 'start'});
}
function scrollDownHome(){
    document.getElementById('home-id').scrollIntoView({ behavior: 'smooth', block: 'start'});
}
function scrollDownSkills(){
    document.getElementById('skills-card').scrollIntoView({ behavior: 'smooth', block: 'start'});
}
// function scrollDownProject(){
//     document.getElementById('home-id').scrollIntoView({ behavior: 'smooth', block: 'start'});
// }
// function scrollDownContact(){
//     document.getElementById('home-id').scrollIntoView({ behavior: 'smooth', block: 'start'});
// }

function activateButton(buttonid,targetid){
    window.addEventListener('scroll', function () {
        const button = document.getElementById(buttonid);
        const target = document.getElementById(targetid);
        const targetPosition = target.getBoundingClientRect().top;

        if (targetPosition < window.innerHeight && targetPosition > 0) {
            button.classList.add('green');
        } else {
            button.classList.remove('green');
        }
    })
}
activateButton("aboutButton",'about-me-id')
activateButton('homeButton','hello-id')
activateButton('skillsButton','skills-card')