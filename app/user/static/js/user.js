$(document).ready(function () {
  // init stat display
  init_stat_display();

  const tabList = [].slice.call(
    document.querySelectorAll('a[data-bs-toggle="tab"]')
  );
  tabList.forEach((tab) => {
    tab.addEventListener("shown.bs.tab", function (e) {
      e.preventDefault();
      const tab_data_name = e.target.id.split("-")[2];
      init_tab_switch(tab_data_name);
    });
  });

  // check if the user is verified
  const usernameInput = document.getElementById("user_name");
  usernameInput.addEventListener("blur", function (e) {
    const username = usernameInput.value;
    verify_user(username);
  });

  const userEmailInput = document.getElementById("user_email");
  userEmailInput.addEventListener("blur", function (e) {
    const email = userEmailInput.value;
    verify_email(email);
  });
});

const init_stat_display = () => {
  $(".count").each(function () {
    const $this = $(this);
    $this.prop("Counter", 0).animate(
      {
        Counter: parseInt($this.text(), 10),
      },
      {
        duration: 1500,
        easing: "linear",
        step: function (now) {
          $this.text(Math.ceil(now));
        },
      }
    );
  });
};

const init_tab_switch = (tab_data_name) => {
  // reset render id and url
  document.getElementById("render-id").innerHTML = `users-${tab_data_name}`;
  document.getElementById(
    "render-url"
  ).innerHTML = `/users/lists?name=${tab_data_name}&page=1`;

  // re-render
  re_render({ page: 1 });
};

//verify user profile - check if the user name exists
const verify_user = async (username) => {
  const response = await getFetch(`/api/v1/users/${username}`)()();
  if (!response.result) {
    // show alert
    const alert = document.getElementById("profileAlert");
    alert.innerHTML = "User exists!";
    if (alert.classList.contains("d-none")) {
      alert.classList.remove("d-none");
    }
    // the alert displays 3s
    setTimeout(() => {
      alert.classList.add("d-none");
    }, 3000);
  }
  // clear the input
  document.getElementById("user_name").value = "";
};

//verify user profile - check if the email exists
const verify_email = async (email) => {
  const response = await getFetch(`/api/v1/users/${email}`)()();
  if (!response.result) {
    // show alert
    const alert = document.getElementById("profileAlert");
    alert.innerHTML = "Email exists!";
    if (alert.classList.contains("d-none")) {
      alert.classList.remove("d-none");
    }
    // the alert displays 3s
    setTimeout(() => {
      alert.classList.add("d-none");
    }, 3000);
  }
  // clear the input
  document.getElementById("user_email").value = "";
};
