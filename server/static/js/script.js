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

// Добавление животного
addAnimalForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем отправку формы const animalName = document.getElementById('animalName').value;
    const animalImage = document.getElementById('animalImage').value;
    const animalAppearance = document.getElementById('animalAppearance').value;
    const animalCharacter = document.getElementById('animalCharacter').value;

    // Создаем карточку животного
    const animalCard = document.createElement('div');
    animalCard.className = 'animal-card';
    animalCard.innerHTML = `
        <img src="${animalImage}" alt="${animalName}" style="width: 100%; border-radius: 10px;">
        <h3>${animalName}</h3>
        <p><strong>Внешность:</strong> ${animalAppearance}</p>
        <p><strong>Характер:</strong> ${animalCharacter}</p>
    `;

    // Добавляем карточку на главный экран
    animalCards.appendChild(animalCard);

    // Закрываем модальное окно
    modal.style.display = 'none';

    // Сбрасываем форму addAnimalForm.reset();
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
