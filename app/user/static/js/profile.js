$(document).ready(function () {
  // init avatar change
  init_avatar_change();

  // check if the user is verified
  const usernameInput = document.getElementById("user_name");
  if (usernameInput === null || usernameInput === undefined) {
    return false;
  }
  usernameInput.addEventListener("blur", function () {
    verify_user(usernameInput);
  });

  // check if the email is verified
  const userEmailInput = document.getElementById("user_email");
  if (userEmailInput === null || userEmailInput === undefined) {
    return false;
  }
  userEmailInput.addEventListener("blur", function () {
    verify_email(userEmailInput);
  });
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
      const avatar = document.getElementById("profileAvatar");
      avatar.src = reader.result;
    };
    reader.readAsDataURL(file);
  });
};

// verify user profile - check if the user name exists
const verify_user = async (usernameInput) => {
  const username = usernameInput.value;
  const current_username = document.getElementById("current_email").innerHTML;
  if (username === current_username) {
    return false;
  }

  const response = await getFetch(`/api/v1/users/username/${username}`)()();
  const result = response.data.result;
  if (!result) {
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
    // clear the input
    document.getElementById("user_name").value = "";
  }
};

// verify user profile - check if the email exists
const verify_email = async (userEmailInput) => {
  const email = userEmailInput.value;
  const current_email = document.getElementById("current_email").innerHTML;
  if (email === current_email) {
    return false;
  }

  const response = await getFetch(`/api/v1/users/email/${email}`)()();
  const result = response.data.result;
  if (!result) {
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
    // clear the input
    document.getElementById("user_email").value = "";
  }
};
