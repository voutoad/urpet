const n_modal = document.getElementById('modal-l');
const loginButton = document.getElementById('login-button');
const n_closeButton = document.getElementById('close-l');


loginButton.addEventListener('click', function() {
    n_modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; 
});


n_closeButton.addEventListener('click', function() {
    n_modal.style.display = 'none';
    document.body.style.overflow = 'auto'; 
});


window.addEventListener('click', function(event) {
    if (event.target === modal) {
        n_modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});