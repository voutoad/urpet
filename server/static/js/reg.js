const modal = document.getElementById('modal');
const regButton = document.getElementById('reg-button');
const closeButton = document.querySelector('.close');


regButton.addEventListener('click', function() {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; 
});


closeButton.addEventListener('click', function() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; 
});


window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});