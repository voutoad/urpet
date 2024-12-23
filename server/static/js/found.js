ymaps.ready(init);

async function init() {
    var myMap = new ymaps.Map("map", {
        center: [55.7522, 37.6156],
        zoom: 10
    });

    // Убираем ненужные элементы управления
    ['zoomControl', 'searchControl', 'rulerControl', 'typeSelector', 'fullscreenControl', 'trafficControl'].forEach(elem => myMap.controls.remove(elem));

    // Пример данных о найденных животных
    // const foundAnimals = [
    //     {
    //         name: 'Кот',
    //         address: 'ул. Чехова, д. 15',
    //         time: '1 день назад',
    //         photo: 'https://placekitten.com/200/300',
    //         description: 'Маленький серый кот с зеленым ошейником.',
    //         coords: [55.7558, 37.6173]
    //     },
    //     {
    //         name: 'Собака',
    //         address: 'ул. Гоголя, д. 8',
    //         time: '3 дня назад',
    //         photo: 'https://placedog.net/200/300',
    //         description: 'Большая черная собака с белой отметиной на груди.',
    //         coords: [55.7583, 37.6175]
    //     }
    // ];
    let resp = await fetch('/get-lost/');
    let foundAnimals = await resp.json();
    // console.log(json);

    const animalNotifications = document.getElementById('animal-notifications');

    foundAnimals.forEach(animal => {
        const notification = document.createElement('div');
        notification.classList.add('notification');
        notification.innerHTML = `
            <img src="/${animal.photo}" alt="${animal.name}">
            <strong>${animal.name}</strong>
            <p>Адрес: ${animal.address}</p>
            <p>Время: ${animal.time}</p>
            <p>${animal.description}</p>
            <button class="remove-button">Убрать с карты</button>
        `;
        animalNotifications.appendChild(notification);
        console.log(animal.coords)
        // Добавление маркера на карту
        const placemark = new ymaps.Placemark([animal.coords[1], animal.coords[0]], {
            balloonContent: `
                <div style="text-align: center;">
                    <strong>${animal.name}</strong><br>
                    <img src="/${animal.photo}" alt="${animal.name}" style="width: 100px; height: auto; border-radius: 5px;"><br>
                    <p>Адрес: ${animal.address}</p>
                    <p>Время: ${animal.time}</p>
                    <p>${animal.description}</p>
                </div>
            `
        }, {
            preset: 'islands#blueCircleDotIconWithCaption',
            iconCaptionMaxWidth: '50'
        });

        myMap.geoObjects.add(placemark);

        // Обработчик кнопки для удаления маркера
        notification.querySelector('.remove-button').addEventListener('click', () => {
            myMap.geoObjects.remove(placemark); // Удалить маркер
            notification.remove(); // Удалить уведомление
            fetch('/admin/delete-form/' + animal.id + '/')
        });
    });
}
