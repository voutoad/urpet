function deleteAnimal(button) {
    const animalDiv = button.parentElement;
    animalDiv.remove();
 // РЎРѕР·РґР°РЅРёРµ СѓРІРµРґРѕРјР»РµРЅРёСЏ
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert';
    alertDiv.innerText = "Р—Р°РїРёСЃСЊ Рѕ Р¶РёРІРѕС‚РЅРѕРј СѓРґР°Р»РµРЅР°.";
    document.body.appendChild(alertDiv);
    
    // РџРѕРєР°Р·Р°С‚СЊ СѓРІРµРґРѕРјР»РµРЅРёРµ
    alertDiv.style.display = 'block';
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 500);
    }, 3000);
}

avatar.addEventListener('click', function() {
    alert('РћС‚РєСЂС‹С‚СЊ Р»РёС‡РЅС‹Р№ РєР°Р±РёРЅРµС‚');
});