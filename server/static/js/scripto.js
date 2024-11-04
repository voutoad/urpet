ymaps.ready(init);

function init(){
    var myMap = new ymaps.Map("map", {
        center: [55.7522, 37.6156],
        zoom: 10
    });
    ['zoomControl', 'searchControl', 'rulerControl',
        'typeSelector', 'fullscreenControl', 'trafficControl'].forEach(elem => myMap.controls.remove(elem));
    
    document.getElementById("address_on_map").addEventListener("click", () => {

        var address = document.getElementById("address_test").value;
        const Http = new XMLHttpRequest();
        const url='https://geocode-maps.yandex.ru/1.x/?apikey=04fcaae6-825a-469a-86fe-eabc5755edd4&geocode=' + address + '&format=json';
        Http.open("GET", url);
        Http.send();
    
        Http.onreadystatechange = (e) => {
            var text = Http.responseText;
            var coords = JSON.parse(text)["response"]["GeoObjectCollection"]["featureMember"]["0"]["GeoObject"]["Point"]["pos"].split(" ");  
            console.log(parseFloat(coords[0]), parseFloat(coords[1]));
            
        myMap.geoObjects.add(new ymaps.Placemark([parseFloat(coords[1]), parseFloat(coords[0])], {
            balloonContent: '<strong>' + "РїР°СЂР°Рј РїР°Рј РїР°Рј" + '</strong>',
        }, {
            preset: 'islands#blueCircleDotIconWithCaption',
            iconCaptionMaxWidth: '50'
        }));
    };
    });
}
document.getElementById("div1").addEventListener("click", () => {
    document.getElementById("popupback1").style.display = "flex";
    document.getElementById("pop1").style.display = "flex";
    document.getElementById("map").style.display = "none";
});

document.getElementById("close1").addEventListener("click", () => {
    document.getElementById("popupback1").style.display = "none";
    document.getElementById("pop1").style.display = "none";
    document.getElementById("map").style.display = "flex";
});

document.getElementById("div2").addEventListener("click", () => {
    document.getElementById("popupback2").style.display = "flex";
    document.getElementById("pop2").style.display = "flex";
    document.getElementById("map").style.display = "none";
});

document.getElementById("close2").addEventListener("click", () => {
    document.getElementById("popupback2").style.display = "none";
    document.getElementById("pop2").style.display = "none";
    document.getElementById("map").style.display = "flex";
});

document.getElementById("div3").addEventListener("click", () => {
    document.getElementById("popupback3").style.display = "flex";
    document.getElementById("pop3").style.display = "flex";
    document.getElementById("map").style.display = "none";
});

document.getElementById("close3").addEventListener("click", () => {
    document.getElementById("popupback3").style.display = "none";
    document.getElementById("pop3").style.display = "none";
    document.getElementById("map").style.display = "flex";
});

document.getElementById("div4").addEventListener("click", () => {
    document.getElementById("popupback4").style.display = "flex";
    document.getElementById("pop4").style.display = "flex";
    document.getElementById("map").style.display = "none";
});

document.getElementById("close4").addEventListener("click", () => {
    document.getElementById("popupback4").style.display = "none";
    document.getElementById("pop4").style.display = "none";
    document.getElementById("map").style.display = "flex";
});