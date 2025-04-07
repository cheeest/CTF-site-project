function showPopup() {
  const popup = document.getElementById("popup");

  popup.classList.remove('slideoutHelp');
  popup.style.display = "block";

  setTimeout(() => {
    popup.classList.add('slideinHelp')
    sqlInpt.classList.add('slideinInpt')
  }, 1);
}

function hidePopup() {
  const popup = document.getElementById("popup");

  popup.classList.remove('slideinHelp');
  popup.classList.add('slideoutHelp');

  setTimeout(() => {
    popup.style.display = "none"
  }, 1000);
}
