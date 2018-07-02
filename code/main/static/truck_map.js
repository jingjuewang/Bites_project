function initialize() {

    getTruckinfo()

    var SanFrancisco = {lat: 37.759851, lng: -122.443782};

    var myOptions = {
        center: SanFrancisco,
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP

    };
    var map = new google.maps.Map(document.getElementById("default"),
        myOptions);

    setMarkers(map, truck_info)
}

function getTruckinfo() {
    return truck_info
}

function setMarkers(map, truck_info) {

    var marker, i
    for (i = 0; i < truck_info.length; i++) {

        var name = truck_info[i].name
        var lat = truck_info[i].lat
        var lng = truck_info[i].lng

        latlngset = new google.maps.LatLng(lat, lng);

        var marker = new google.maps.Marker({
            map: map, title: name, position: latlngset
        });
        map.setCenter(marker.getPosition())

        var content = "Name: " + name

        var infowindow = new google.maps.InfoWindow()


        google.maps.event.addListener(marker,'mouseover', (function(marker,content,infowindow){ 
            return function() {
                infowindow.setContent(content);
                infowindow.open(map,marker);
            };
        })(marker,content,infowindow));

        google.maps.event.addListener(marker,'mouseout', (function(marker,content,infowindow){ 
            return function() {
                infowindow.close(map,marker);
            };
        })(marker,content,infowindow));

    }
}

