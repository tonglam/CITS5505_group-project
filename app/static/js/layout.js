$(document).ready(function () {
  const { Input, Tab, Dropdown, Tooltip, Ripple, initMDB } = mdb;
  initMDB({ Input, Tab, Dropdown, Tooltip, Ripple });

  window.setTimeout(function () {
    let alertElement = document.getElementById("alert");
    if (typeof alertElement != "undefined" && alertElement != null) {
      document.getElementById("alert").classList.add("d-none");
    }
  }, 2500);
});
