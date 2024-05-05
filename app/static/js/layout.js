$(document).ready(function () {
  // alert
  init_alert();
});

const init_alert = () => {
  window.setTimeout(function () {
    let alertElement = document.getElementById("alert");
    if (typeof alertElement != "undefined" && alertElement != null) {
      document.getElementById("alert").classList.add("d-none");
    }
  }, 2500);
};
