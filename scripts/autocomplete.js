const options = {country: "us"};
const address = document.getElementById("address");
const acFromAddress = new google.maps.places.Autocomplete(address, options);
const address_form = document.getElementById("address_form");

const form = document.getElementById("address_form");
form.addEventListener("keypress", function(e){
  if(e.keyCode == 13){
    e.preventDefault()
  };
});
