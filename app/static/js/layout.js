$(document).ready(function () {
  // nav active
  init_nav_active();
  // alert
  init_alert();
  // search
  init_search();
});

const init_nav_active = () => {
  const navItems = document.querySelectorAll(".nav-menu");
  navItems.forEach((navItem) => {
    const navLink = navItem.querySelector(".nav-link");
    if (!navLink) {
      return;
    }
    const activeItem = get_nav_item();
    if (navLink.textContent.trim() === activeItem) {
      navLink.classList.add("active");
    } else {
      navLink.classList.remove("active");
    }
  });
};

const get_nav_item = () => {
  const path = window.location.pathname;
  if (path.includes("/populars")) {
    return "Popular";
  } else if (path.includes("/communities")) {
    return "Community";
  }
  return "Home";
};

const init_alert = () => {
  window.setTimeout(function () {
    const alertElement = document.getElementById("alert");
    if (typeof alertElement != "undefined" && alertElement != null) {
      document.getElementById("alert").classList.add("d-none");
    }
  }, 2500);
};

const init_search = () => {
  const search = document.getElementById("search");
  search.addEventListener("focus", function () {
    location.href = "/search";
  });
};

const handle_page_click = async (page, scrollId) => {
  if (page === undefined || page === null || page === "") {
    console.error("page", page);
    return false;
  }

  // get render id
  const render_id = document.getElementById("render-id").textContent;
  if (render_id === "undefined" || render_id === null || render_id === "") {
    console.error("render id is missing");
    return false;
  }

  // current page do not fetch again
  const current_page = document
    .getElementById(render_id)
    .querySelector(".page-item.active")
    .querySelector("a").textContent;
  if (page === parseInt(current_page)) {
    console.error(
      "current page is the same with navigate page: ",
      current_page
    );
    return false;
  }

  // re-render
  re_render({ page: page });

  // scroll to
  const element = document.getElementById(scrollId);
  if (element === undefined || element === null) {
    window.scrollTo(0, 0);
    return false;
  }
  element.scrollIntoView({
    behavior: "smooth",
    block: "start",
    inline: "nearest",
  });
};

const re_render = async (paramsToAdd = {}, keysToRemove = []) => {
  // get render id
  const render_id = document.getElementById("render-id").textContent;
  if (render_id === "undefined" || render_id === null || render_id === "") {
    console.error("render id is missing");
    return false;
  }

  // get render url
  let render_url = document.getElementById("render-url").textContent;
  if (render_url === undefined || render_url === null || render_url === "") {
    console.error("render url is missing");
    return false;
  }

  // create new render url
  let new_render_url;

  // add specified parameters
  if (Object.keys(paramsToAdd).length > 0) {
    new_render_url = create_add_param_render_url(render_url, paramsToAdd);
  }

  // remove specified parameters
  if (keysToRemove.length > 0) {
    new_render_url = create_remove_param_render_url(
      new_render_url,
      keysToRemove
    );
  }

  // update render url
  document.getElementById("render-url").innerHTML = new_render_url;

  // fetch page content
  const response = await getFetch(new_render_url)()();
  if (response === undefined || response === null || response === "") {
    console.error("re-render response is missing");
    return false;
  }

  // re-render search results, client side rendering here
  document.getElementById(render_id).innerHTML = response;
};

const create_add_param_render_url = (render_url, paramsArray) => {
  const url = new URL(render_url, window.location.origin);

  const params = url.searchParams;
  Object.entries(paramsArray).forEach(([key, value]) => {
    params.set(key, value);
  });
  url.search = params.toString();

  return `${url.pathname}${url.search}${url.hash}`;
};

const create_remove_param_render_url = (render_url, keyArray) => {
  const url = new URL(render_url, window.location.origin);

  const params = url.searchParams;
  keyArray.forEach((key) => {
    params.delete(key);
  });
  url.search = params.toString();

  return `${url.pathname}${url.search}${url.hash}`;
};

const handle_user_profile_click = async () => {
  const user_profile_card = document.getElementById("userProfileCard");

  // display user profile card
  const user_profile = document.getElementById("navUserProfile");
  if (user_profile === undefined || user_profile === null) {
    return false;
  }

  if (user_profile_card.classList.contains("d-none")) {
    user_profile_card.classList.remove("d-none");
  } else {
    user_profile_card.classList.add("d-none");
  }

  // close user profile card
  document
    .getElementById("closeUserProfile")
    .addEventListener("click", function () {
      user_profile_card.classList.add("d-none");
    });
};

const handle_notification_click = async () => {
  const notice = document.getElementById("notice");
  if (notice === undefined || notice === null) {
    console.error("notice is missing");
    return false;
  }

  // check if notification number is 0
  const spanBadge = notice.querySelector("span");
  if (spanBadge === undefined || spanBadge === null) {
    return false;
  }

  // nav bar notification
  const notification = document.getElementById("notification");
  if (notification === undefined || notice === null) {
    console.error("notification is missing");
    return false;
  }

  if (notification.classList.contains("d-none")) {
    notification.classList.remove("d-none");
  } else {
    notification.classList.add("d-none");
  }
};

const handle_notification_change = (notice_id) => {
  // check for notification
  const check_notification = document.getElementById("notice-" + notice_id);
  if (check_notification === undefined || check_notification === null) {
    console.error("check_notification is missing");
    return false;
  }

  // wait for 2s, if no more click, close notification
  setTimeout(() => {
    // call api to update notification
    update_notification(notice_id);
    // re-render notification
    re_render_notification();
  }, 1000);
};

const update_notification = async (notice_id) => {
  await putFetch(`/api/v1/users/notifications/${notice_id}`)()();
};

const re_render_notification = async () => {
  const spanBadge = document.getElementById("notice").querySelector("span");
  if (spanBadge === undefined || spanBadge === null) {
    console.error("spanBadge is missing");
    return false;
  }
  let notification_num = parseInt(spanBadge.textContent);
  setTimeout(async () => {
    const response = await getFetch(`/notifications`)()();
    // re-render notification
    document.getElementById("notification").innerHTML = response;
    // re-render navbar notification
    notification_num -= 1;
    const spanBadge = document.getElementById("notice").querySelector("span");
    spanBadge.textContent = notification_num;
    if (notification_num === 0) {
      // hide notification badge
      spanBadge.classList.add("d-none");
      // close notification
      document.getElementById("notification").classList.add("d-none");
    }
  }, 500);
};

const handle_close_notification = () => {
  // close notification
  const notification_close = document.getElementById("closeNotification");
  if (notification_close === undefined || notification_close === null) {
    console.error("notification_close is missing");
    return false;
  }

  notification_close.addEventListener("click", function () {
    notification.classList.add("d-none");
  });
};
