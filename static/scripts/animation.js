function showPopup() {
  const popup = document.getElementById("popup");
  const sqlInpt = document.getElementById("sqlInpt");

  popup.classList.remove('slideoutHelp');
  sqlInpt.classList.remove('slideoutInpt');
  popup.style.display = "block";

  setTimeout(() => {
    popup.classList.add('slideinHelp')
    sqlInpt.classList.add('slideinInpt')
  }, 1);
}

function hidePopup() {
  const popup = document.getElementById("popup");
  const sqlInpt = document.getElementById("sqlInpt");

  sqlInpt.classList.remove('slideinInpt');
  sqlInpt.classList.add('slideoutInpt')
  popup.classList.remove('slideinHelp');
  popup.classList.add('slideoutHelp');

  setTimeout(() => {
    popup.style.display = "none"
    popup.style.position = "absolute"
  }, 1000);
}
