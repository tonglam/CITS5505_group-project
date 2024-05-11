$(document).ready(function () {
  // check if the user is verified
  const usernameInput = document.getElementById("user_name");
  usernameInput.addEventListener("blur", function () {
    verify_user(usernameInput);
  });

  // check if the email is verified
  const userEmailInput = document.getElementById("user_email");
  userEmailInput.addEventListener("blur", function () {
    verify_email(userEmailInput);
  });

  // check if the password is verified
  const passwordInput = document.getElementById("user_password");
  passwordInput.addEventListener("blur", function () {
    verify_password(passwordInput);
  });
});

// verify user profile - check if the user name exists
const verify_user = async (usernameInput) => {
  const username = usernameInput.value;
  const current_userneme = document.getElementById("current_email").innerHTML;
  if (username === current_userneme) {
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

// verify user profile - check if the password is valid
const verify_password = (passwordInput) => {
  const password = passwordInput.value;
  if (password.length < 8) {
    // show alert
    const alert = document.getElementById("profileAlert");
    alert.innerHTML = "Password must be at least 8 characters!";
    if (alert.classList.contains("d-none")) {
      alert.classList.remove("d-none");
    }
    // the alert displays 3s
    setTimeout(() => {
      alert.classList.add("d-none");
    }, 3000);
    // clear the input
    document.getElementById("user_password").value = "";
  }
};
