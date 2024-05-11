$(document).ready(function () {
  // alert
  init_alert();
  // search
  init_search();
  // notification
  init_notification();
});

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

const handle_page_click = async (page) => {
  if (page === undefined || page === null || page === "") {
    console.log("page", page);
    return false;
  }

  // current page do not fetch again
  current_page = document
    .querySelector(".page-item.active")
    .querySelector("a").textContent;
  if (page === parseInt(current_page)) {
    return false;
  }

  // re-render
  re_render({ page: page });
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

const init_notification = () => {
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

  const notification = document.getElementById("notification");
  if (notification === undefined || notice === null) {
    console.error("notification is missing");
    return false;
  }

  // nav bar notification
  notice.addEventListener("click", function () {
    if (notification.classList.contains("d-none")) {
      notification.classList.remove("d-none");
    } else {
      notification.classList.add("d-none");
    }
  });
};

const handle_notification_change = (notice_id) => {
  // check for notification
  const check_notification = document.getElementById(
    "notificationCheck-" + notice_id
  );
  if (check_notification === undefined || check_notification === null) {
    console.error("check_notification is missing");
    return false;
  }

  if (check_notification.classList.contains("unchecked")) {
    handle_notification_checked(check_notification);
  } else if (check_notification.classList.contains("checked")) {
    handle_notification_unchecked(check_notification);
  }

  // wait for 2s, if no more click, close notification
  setTimeout(() => {
    if (check_notification.classList.contains("checked")) {
      // call api to update notification
      update_notification(notice_id);
      // re-render notification
      re_render_notification();
    }
  }, 1000);
};

const handle_notification_checked = async (check_notification) => {
  check_notification.classList.remove("unchecked");
  check_notification.classList.add("checked");
  // replace icon
  check_notification.innerHTML = `<i class="fa-regular fa-square-check fa-xl"></i>`;
};

const handle_notification_unchecked = async (check_notification) => {
  check_notification.classList.remove("checked");
  check_notification.classList.add("unchecked");
  // replace icon
  check_notification.innerHTML = `<i class="fa-regular fa-square fa-xl"></i>`;
};

const update_notification = async (notice_id) => {
  const response = await putFetch(
    `/api/v1/users/notifications/${notice_id}`
  )()();
};

const re_render_notification = async () => {
  setTimeout(async () => {
    const response = await getFetch(`/notifications`)()();
    // re-render notification
    document.getElementById("notification").innerHTML = response;
    // re-render navbar notification
    const notification_num = parseInt(
      document.getElementById("notification-num").textContent
    );
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

const upload_image = async (formData) => {
  const response = postFetch("/api/v1/upload/image")(formData);
  console.log("response", response);
  return response;
};
