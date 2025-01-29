(function(window, document, undefined) {

  // code that should be taken care of right away

  window.onload = init;

  function init(){
    const popup = document.getElementById("popup");
    const help = document.getElementById("help");
    const sqlInpt = document.getElementById("sqlInpt");

    function showPopup() {
      popup.classList.remove('slideoutHelp');
      sqlInpt.classList.remove('slideoutInpt');
      popup.style.display = "block";
      setTimeout(() => popup.classList.add('slideinHelp'), 1);
      setTimeout(() => sqlInpt.classList.add('slideinInpt'), 1);
    }

    function hidePopup() {
      sqlInpt.classList.remove('slideinInpt');
      popup.classList.remove('slideinHelp');
      setTimeout(() => {popup.style.display = "none"}, 1000);
      setTimeout(() => {popup.style.position = "absolute"}, 1000);
      popup.classList.add('slideoutHelp');
      sqlInpt.classList.add('slideoutInpt')
    }

    help.addEventListener("click", showPopup);
    popup.addEventListener("click", hidePopup);
  }

})(window, document, undefined);

