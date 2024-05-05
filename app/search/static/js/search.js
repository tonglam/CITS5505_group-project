import { getFetch } from "../../../static/js/fetch.js";

$(document).ready(function () {
  // disable navbar search input
  document.getElementById("search").disabled = true;

  // focus search input
  document.getElementById("searchInput").focus();

  // init search
  init_search();

  // handle search click
  document
    .getElementById("searchButton")
    .addEventListener("click", function () {
      handle_search_click();
    });
});

const init_search = async () => {
  let searchInputElement = document.getElementById("searchInput");
  if (searchInputElement === null) {
    return false;
  }

  searchInputElement.addEventListener("keyup", async function () {
    const keyword = this.value.toLowerCase().trim();
    search_fetch(keyword);
  });
};

const handle_search_click = async () => {
  console.log("search button clicked");
  const keyword = document
    .getElementById("searchInput")
    .value.toLowerCase()
    .trim();
  search_fetch(keyword);
};

const search_fetch = async (keyword) => {
  // becase Flask does not support partial rendering
  // we need to call the partial template from the server side
  const url = "/search/results";
  const data = { keyword: keyword };
  const response = await getFetch(url)(data)();

  // re-render search results, client side rendering here
  document.getElementById("searchResults").innerHTML = response;
};
