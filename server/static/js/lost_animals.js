// Получаем элементы
const lostAnimalRequests = document.getElementById('lostAnimalRequests');

// Обработчики для каждой заявки
const requests = lostAnimalRequests.getElementsByClassName('lost-animal');

for (let request of requests) {
    // Обработчик для удаления заявки
    const deleteButton = request.querySelector('.delete-button');
    deleteButton.addEventListener('click', function() {
        id = request.id
        fetch("http://127.0.0.1:8000/admin/delete-form/" + id + "/");
        lostAnimalRequests.removeChild(request);
        
    });

    // Обработчик для отметки заявки как выполненной
    const checkbox = request.querySelector('.request-checkbox');
    checkbox.addEventListener('change', function() {
        if (checkbox.checked) {
            id = request.id
            fetch("http://127.0.0.1:8000/admin/change-form/" + id + "/");
            lostAnimalRequests.removeChild(request);
        }
    });
}
