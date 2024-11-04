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

            balloonContent: '<strong>' + "парам пам пам" + '</strong>',

        }, {

            preset: 'islands#blueCircleDotIconWithCaption',

            iconCaptionMaxWidth: '50'

        }));

    };

    });

}