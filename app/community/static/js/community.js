$(document).ready(function () {
  // init avatar change
  init_avatar_change();
  // text area auto resize
  init_textarea_auto_resize();
});

const init_avatar_change = () => {
  const avatarInput = document.getElementById("avatarInput");
  if (avatarInput === null || avatarInput === undefined) {
    return false;
  }
  avatarInput.addEventListener("change", function () {
    const file = avatarInput.files[0];
    const reader = new FileReader();
    reader.onload = function () {
      const avatar = document.getElementById("communityAvatar");
      avatar.src = reader.result;
    };
    reader.readAsDataURL(file);
  });
};

const handle_join_community = async (id) => {
  const response = await postFetch(`/api/v1/communities/${id}/join`)()();
  if (response.code === 200) {
    const current_page = get_current_page();
    re_render_community_list(current_page);
    re_render_navbar();
  } else if (response.code === 400) {
    display_alert("You are already in this community");
  } else if (response.code === 404) {
    display_alert("Community not found");
  }
};

const handle_leave_community = async (id) => {
  const response = await postFetch(`/api/v1/communities/${id}/leave`)()();
  if (response.code === 200) {
    const current_page = get_current_page();
    re_render_community_list(current_page);
    re_render_navbar();
  } else if (response.code === 400) {
    display_alert("You are not in this community");
  } else if (response.code === 404) {
    display_alert("Community not found");
  }
};

const handle_delete_community = async (id) => {
  const response = await deleteFetch(`/api/v1/communities/${id}/delete`)()();
  if (response.code === 204) {
    re_render_community_list(1);
    re_render_navbar();
  } else if (response.code === 404) {
    display_alert("Community not found");
  } else if (response.code === 403) {
    display_alert("You are not the owner of this community");
  }
};

const get_current_page = () => {
  return document.querySelector(".page-item.active").querySelector("a")
    .textContent;
};

const re_render_community_list = async (page) => {
  const response = await getFetch(`/communities/community_list`)({
    page: page,
  })();
  document.getElementById("community-list").innerHTML = response;
};

const display_alert = (message) => {
  // show alert
  const alert = document.getElementById("communityAlert");
  alert.innerHTML = message;
  if (alert.classList.contains("d-none")) {
    alert.classList.remove("d-none");
  }
  // the alert displays 3s
  setTimeout(() => {
    alert.classList.add("d-none");
  }, 3000);
};

const re_render_navbar = async () => {
  const response = await getFetch(`/navbar`)()();
  document.getElementById("navMenu").innerHTML = response;
};

const init_textarea_auto_resize = () => {
  const textAreas = document.querySelectorAll("textarea");
  textAreas.forEach((textArea) => {
    textArea.style.height = "auto";
    textArea.style.height = textArea.scrollHeight + "px";
    textArea.addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });
  });
};
