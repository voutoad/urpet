document.addEventListener('DOMContentLoaded', function() {
    const approveButtons = document.querySelectorAll('.approve-button');
    const rejectButtons = document.querySelectorAll('.reject-button');
    const popup = document.getElementById('popup');
    const emailToSend = document.getElementById('emailToSend');
    const closePopup = document.getElementById('closePopup');
    const sendEmailButton = document.getElementById('sendEmailButton');

    approveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const request = this.closest('.volunteer-request');
            const email = request.getAttribute('data-email');
            emailToSend.textContent = email;
            popup.style.display = 'flex';

            sendEmailButton.onclick = function() {
                alert(`РџРёСЃСЊРјРѕ РѕС‚РїСЂР°РІР»РµРЅРѕ РЅР° ${email}`);
                request.remove(); // РЈРґР°Р»СЏРµРј Р·Р°СЏРІРєСѓ РїРѕСЃР»Рµ РѕРґРѕР±СЂРµРЅРёСЏ popup.style.display = 'none';
            };
        });
    });

    rejectButtons.forEach(button => {
        button.addEventListener('click', function() {
            const request = this.closest('.volunteer-request');
            request.remove(); // РЈРґР°Р»СЏРµРј Р·Р°СЏРІРєСѓ РїРѕСЃР»Рµ РѕС‚РєР°Р·Р°
        });
    });

    closePopup.addEventListener('click', function() {
        popup.style.display = 'none';
    });

    window.onclick = function(event) {
        if (event.target === popup) {
            popup.style.display = 'none';
        }
    };
});


// Р›РёС‡РЅС‹Р№ РєР°Р±РёРЅРµС‚ (РїРѕРєР° РїСЂРѕСЃС‚Рѕ РІС‹РІРѕРґРёРј СЃРѕРѕР±С‰РµРЅРёРµ)
avatar.addEventListener('click', function() {
    alert('РћС‚РєСЂС‹С‚СЊ Р»РёС‡РЅС‹Р№ РєР°Р±РёРЅРµС‚');
});