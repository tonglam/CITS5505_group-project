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
  try {
    const response = await postFetch(`/api/v1/communities/${id}/join`)()();
    const jsonResponse = await response.json();

    if (jsonResponse.code === 200) {
      // Update button state immediately
      const button = document.querySelector(
        `button[onclick="handle_join_community(${id})"]`
      );
      if (button) {
        button.onclick = () => handle_leave_community(id);
        button.textContent = "Leave";
      }

      // Re-render other parts if needed
      const current_page = get_current_page();
      if (current_page === -1) {
        window.location.reload();
        return;
      }
      await re_render_community_list(current_page);
      await re_render_navbar();
    } else if (jsonResponse.code === 400) {
      display_alert("You are already in this community");
    } else if (jsonResponse.code === 404) {
      display_alert("Community not found");
    }
  } catch (error) {
    console.error("Error joining community:", error);
    display_alert("Failed to join community");
  }
};

const handle_leave_community = async (id) => {
  try {
    const response = await postFetch(`/api/v1/communities/${id}/leave`)()();
    const jsonResponse = await response.json();

    if (jsonResponse.code === 200) {
      // Update button state immediately
      const button = document.querySelector(
        `button[onclick="handle_leave_community(${id})"]`
      );
      if (button) {
        button.onclick = () => handle_join_community(id);
        button.textContent = "Join";
      }

      // Re-render other parts if needed
      const current_page = get_current_page();
      if (current_page === -1) {
        window.location.reload();
        return;
      }
      await re_render_community_list(current_page);
      await re_render_navbar();
    } else if (jsonResponse.code === 400) {
      display_alert("You are not in this community");
    } else if (jsonResponse.code === 404) {
      display_alert("Community not found");
    }
  } catch (error) {
    console.error("Error leaving community:", error);
    display_alert("Failed to leave community");
  }
};

const get_current_page = () => {
  const activePage = document.querySelector(".page-item.active");
  if (activePage === null || activePage === undefined) {
    return -1;
  }
  const element = activePage.querySelector("a");
  if (element === null || element === undefined) {
    return -1;
  }
  return element.textContent;
};

const re_render_community_list = async (page) => {
  try {
    const response = await getFetch(`/communities/community_list`)({
      page: page,
    })();
    if (!response || !response.ok) {
      console.error("Failed to get community list:", response);
      return false;
    }
    const responseText = await response.text();

    // re-render community list
    const communityList = document.getElementById("community-list");
    if (communityList) {
      communityList.innerHTML = responseText;
    }
  } catch (error) {
    console.error("Error re-rendering community list:", error);
    return false;
  }
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
  const response = await getFetch("/navbar")()();
  if (!response || !response.ok) {
    console.error("Failed to get navbar:", response);
    return false;
  }
  const responseText = await response.text();

  // re-render navbar
  const navbar = document.getElementById("navMenu");
  if (navbar) {
    navbar.innerHTML = responseText;
  }
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
