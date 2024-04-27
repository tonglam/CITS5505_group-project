$(document).ready(function () {
  window.setTimeout(function () {
    let alertElement = document.getElementById("alert");
    if (typeof alertElement != "undefined" && alertElement != null) {
      document.getElementById("alert").classList.add("d-none");
    }
  }, 2500);
});
