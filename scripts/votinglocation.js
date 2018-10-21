const mapTo = document.getElementById("address");

console.log(mapTo);

var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 2
    // origin: mapFrom
    // destination: mapTo
  });
}
