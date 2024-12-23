// Получаем элементы
const lostAnimalRequests = document.getElementById("foundAnimalsContainer");
// console.log(document);
// Обработчики для каждой заявки
const requests = lostAnimalRequests.getElementsByClassName("found-animal");

for (let request of requests) {
  // Обработчик для удаления заявки
  const deleteButton = request.querySelector(".delete-button");
  deleteButton.addEventListener("click", function () {
    id = request.id;
    fetch("/admin/delete-form/" + id + "/");
    lostAnimalRequests.removeChild(request);
  });

  // Обработчик для отметки заявки как выполненной
  const checkbox = request.querySelector(".request-checkbox");
  checkbox.addEventListener("change", function () {
    if (checkbox.checked) {
      id = request.id;
      fetch("/admin/change-form/" + id + "/");
      lostAnimalRequests.removeChild(request);
    }
  });
}
