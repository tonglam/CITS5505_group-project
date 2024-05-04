$(document).ready(function () {
  // alert
  init_alert();
  // search
  init_search_input();
});

const init_alert = () => {
  window.setTimeout(function () {
    let alertElement = document.getElementById("alert");
    if (typeof alertElement != "undefined" && alertElement != null) {
      document.getElementById("alert").classList.add("d-none");
    }
  }, 2500);
};

const handleSearchFocus = () => {
  // init search display
  init_search_display();

  // search component
  init_search();
};

const init_search_display = () => {
  // hide navbar search input
  let searchElement = document.getElementById("search");
  searchElement.disabled = true;

  // hide page content
  let pageContent = document.getElementById("pageContent");
  pageContent.classList.add("d-none");

  // show search component
  searchComponent.classList.remove("d-none");
};

const end_search_display = () => {
  // hide search component
  searchComponent.classList.add("d-none");

  // show navbar search input
  let searchElement = document.getElementById("search");
  searchElement.disabled = false;

  // show page content
  let pageContent = document.getElementById("pageContent");
  pageContent.classList.remove("d-none");
};

const init_search = () => {
  let searchInput = document.getElementById("searchInput");
  if (searchInput === null) {
    return false;
  }

  searchInput.focus();

  hide_search_component();
};

const hide_search_component = () => {
  let main = document.getElementById("main");
  main.classList.add("pe-none");

  let overlay = document.getElementById("overlay");
  let overlayContent = document.getElementById("overlayContent");

  // hide search component overlap
  document.addEventListener("click", function () {
    overlay.classList.add("d-none");
    main.classList.remove("pe-none");
    end_search_display();
  });

  // do not apply when click the search card
  overlayContent.addEventListener("click", function (event) {
    event.stopPropagation();
  });
};

const init_search_input = () => {
  let searchInputElement = document.getElementById("searchInput");
  if (searchInputElement === null) {
    return false;
  }

  searchInputElement.addEventListener("keyup", function () {
    let value = this.value.toLowerCase().trim();
    console.log("value:" + value);
  });
};
