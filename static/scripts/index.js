(function(window, document, undefined) {

  // code that should be taken care of right away

  window.onload = init;

  function init(){
    const popup = document.getElementById("popup");
    const help = document.getElementById("help");

    function showPopup() {
      popup.style.display = "block";
      console.log('cat')
    }

    function hidePopup() {
      popup.style.display = "none";
    }

    help.addEventListener("click", showPopup);
    popup.addEventListener("click", hidePopup);
  }

})(window, document, undefined);

