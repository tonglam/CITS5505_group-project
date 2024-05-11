$(document).ready(function () {
  // alert
  init_alert();
  // search
  init_search();
});

const init_alert = () => {
  window.setTimeout(function () {
    let alertElement = document.getElementById("alert");
    if (typeof alertElement != "undefined" && alertElement != null) {
      document.getElementById("alert").classList.add("d-none");
    }
  }, 2500);
};

const init_search = () => {
  let search = document.getElementById("search");
  search.addEventListener("focus", function (event) {
    location.href = "/search";
  });
};
