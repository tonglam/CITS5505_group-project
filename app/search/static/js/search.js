import { getFetch } from "../../../static/js/fetch.js";

$(document).ready(function () {
  // disable navbar search input
  let searchElement = document.getElementById("search");
  searchElement.disabled = true;

  // focus search input
  let searchInput = document.getElementById("searchInput");
  searchInput.focus();

  // init search
  init_search();
});

const init_search = async () => {
  let searchInputElement = document.getElementById("searchInput");
  if (searchInputElement === null) {
    return false;
  }

  searchInputElement.addEventListener("keyup", async function () {
    let keyword = this.value.toLowerCase().trim();

    // becase Flask does not support partial rendering, we need to call the partial template from the server side
    const url = "/search/results";
    const data = { keyword: keyword };
    await getFetch(url)(data)();
  });
};
