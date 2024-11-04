// РџРѕР»СѓС‡Р°РµРј СЌР»РµРјРµРЅС‚С‹
const modal = document.getElementById('addAnimalModal');
const addAnimalButton = document.getElementById('addAnimalButton');
const closeModal = document.getElementById('closeModal');
const addAnimalForm = document.getElementById('addAnimalForm');
const animalCards = document.getElementById('animalCards');
const avatar = document.getElementById('avatar');

// РћС‚РєСЂС‹С‚РёРµ РјРѕРґР°Р»СЊРЅРѕРіРѕ РѕРєРЅР°
addAnimalButton.addEventListener('click', function(event) {
    event.preventDefault(); // РџСЂРµРґРѕС‚РІСЂР°С‰Р°РµРј РїРµСЂРµС…РѕРґ РїРѕ СЃСЃС‹Р»РєРµ
    modal.style.display = 'flex';
});

// Р—Р°РєСЂС‹С‚РёРµ РјРѕРґР°Р»СЊРЅРѕРіРѕ РѕРєРЅР°
closeModal.addEventListener('click', function() {
    modal.style.display = 'none';
});

// Р”РѕР±Р°РІР»РµРЅРёРµ Р¶РёРІРѕС‚РЅРѕРіРѕ
addAnimalForm.addEventListener('submit', function(event) {
    event.preventDefault(); // РџСЂРµРґРѕС‚РІСЂР°С‰Р°РµРј РѕС‚РїСЂР°РІРєСѓ С„РѕСЂРјС‹ const animalName = document.getElementById('animalName').value;
    const animalImage = document.getElementById('animalImage').value;
    const animalName = document.getElementById('animalName').value;
    const animalAppearance = document.getElementById('animalAppearance').value;
    const animalCharacter = document.getElementById('animalCharacter').value;

    // РЎРѕР·РґР°РµРј РєР°СЂС‚РѕС‡РєСѓ Р¶РёРІРѕС‚РЅРѕРіРѕ
    const animalCard = document.createElement('div');
    animalCard.className = 'animal-card';
    animalCard.innerHTML = `
        <img src="${animalImage}" alt="${animalName}" style="width: 100%; border-radius: 10px;">
        <h3>${animalName}</h3>
        <p><strong>Р’РЅРµС€РЅРѕСЃС‚СЊ:</strong> ${animalAppearance}</p>
        <p><strong>РҐР°СЂР°РєС‚РµСЂ:</strong> ${animalCharacter}</p>
    `;

    // Р”РѕР±Р°РІР»СЏРµРј РєР°СЂС‚РѕС‡РєСѓ РЅР° РіР»Р°РІРЅС‹Р№ СЌРєСЂР°РЅ
    animalCards.appendChild(animalCard);

    // Р—Р°РєСЂС‹РІР°РµРј РјРѕРґР°Р»СЊРЅРѕРµ РѕРєРЅРѕ
    modal.style.display = 'none';

    // РЎР±СЂР°СЃС‹РІР°РµРј С„РѕСЂРјСѓ addAnimalForm.reset();
});

// Р—Р°РєСЂС‹С‚РёРµ РјРѕРґР°Р»СЊРЅРѕРіРѕ РѕРєРЅР° РїСЂРё РєР»РёРєРµ РІРЅРµ РµРіРѕ
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

// Р›РёС‡РЅС‹Р№ РєР°Р±РёРЅРµС‚ (РїРѕРєР° РїСЂРѕСЃС‚Рѕ РІС‹РІРѕРґРёРј СЃРѕРѕР±С‰РµРЅРёРµ)
avatar.addEventListener('click', function() {
    alert('РћС‚РєСЂС‹С‚СЊ Р»РёС‡РЅС‹Р№ РєР°Р±РёРЅРµС‚');
});