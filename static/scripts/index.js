(function(window, document, undefined) {

  // code that should be taken care of right away

  window.onload = init;

  function init(){
    const popupOverlay = document.getElementById("popup-overlay");
    const popup = document.getElementById("popup");
    const help = document.getElementById("help");

    function showPopup() {
      popupOverlay.style.display = "block";
    }

    function hidePopup() {
      popupOverlay.style.display = "none";
    }

    help.addEventListener("click", showPopup);
    popupOverlay.addEventListener("click", hidePopup);
    popup.addEventListener("click", (event) => event.stopPropagation());
  }

})(window, document, undefined);

