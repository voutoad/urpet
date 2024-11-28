document.addEventListener('DOMContentLoaded', function() {
    const userInfoForm = document.getElementById('user-info');
    const animalList = document.getElementById('animal-list');

    // Обработчик отправки формы
    userInfoForm.addEventListener('submit', function(event) {
        event.preventDefault();
        alert('Ваши данные сохранены!');
    });

    // Пример уведомлений о достижениях
    const achievements = [
        { message: 'Вы нашли 5 животных!', icon: 'https://img.icons8.com/emoji/48/000000/paw-prints.png' },
        { message: 'Вы помогли 10 питомцам найти дом!', icon: 'https://img.icons8.com/emoji/48/000000/dog.png' },
        { message: 'Вы зарегистрировались на сайте!', icon: 'https://img.icons8.com/emoji/48/000000/cat.png' },
    ];

    // Отображение уведомлений
    achievements.forEach(ach => {
        const notification = document.createElement('div');
        notification.classList.add('notification');
        notification.innerHTML = `<img src="${ach.icon}" alt="icon">${ach.message}`;
        animalList.appendChild(notification);
    });
});
