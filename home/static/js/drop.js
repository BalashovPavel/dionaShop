/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunctionDrop() {
    document.getElementById("myDropdown").classList.toggle("show");
    document.getElementById("listDropdown").classList.toggle("current");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    document.getElementById("listDropdown").classList.remove("current");

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}