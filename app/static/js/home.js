$(document).ready(function () {
  // community select
  init_community_select();

  // sort select
  init_sort_select();
});

const init_community_select = () => {
  const communitySelect = document.getElementById("community-select");

  if (communitySelect === "undefined" || communitySelect === null) {
    return false;
  }

  communitySelect.addEventListener("change", function () {
    const community_id =
      communitySelect.options[communitySelect.selectedIndex].id;

    if (community_id === "undefined" || community_id === null) {
      console.error("community id is missing");
      return false;
    }

    if (community_id === "all-community") {
      // reset page to 1 and re-render
      re_render({ page: 1 }, ["community_id"]);
    } else {
      // reset page to 1 and re-render
      re_render({ community_id: community_id, page: 1 });
    }
  });
};

const init_sort_select = () => {
  const sortSelect = document.getElementById("sort-select");

  if (sortSelect === "undefined" || sortSelect === null) {
    return false;
  }

  sortSelect.addEventListener("change", function () {
    const order_by = sortSelect.options[sortSelect.selectedIndex].id;

    if (order_by === "undefined" || order_by === null) {
      console.error("community id is missing");
      return false;
    }

    if (order_by === "all-sort") {
      // reset page to 1 and re-render
      re_render({ page: 1 }, ["order_by"]);
    } else {
      // reset page to 1 and re-render
      re_render({ order_by: order_by, page: 1 });
    }
  });
};
