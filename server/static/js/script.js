// Получаем элементы
const modal = document.getElementById('addAnimalModal');
const addAnimalButton = document.getElementById('addAnimalButton');
const closeModal = document.getElementById('closeModal');
const addAnimalForm = document.getElementById('addAnimalForm');
const animalCards = document.getElementById('animalCards');
const avatar = document.getElementById('avatar');

// Открытие модального окна
addAnimalButton.addEventListener('click', function(event) {
    event.preventDefault(); // Предотвращаем переход по ссылке
    modal.style.display = 'flex';
});

// Закрытие модального окна
closeModal.addEventListener('click', function() {
    modal.style.display = 'none';
});

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

// Личный кабинет (пока просто выводим сообщение)
avatar.addEventListener('click', function() {
    alert('Открыть личный кабинет');
});
