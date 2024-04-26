$(document).ready(function () {
  $("#email").on("blur", function () {
    checkEmail(this.value);
  });
});

async function checkEmail(email) {
  console.log("checkEmail", email);
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailRegex.test(email)) {
    console.log("Valid email");
  } else {
    console.log("Invalid email");
  }
}

const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("login_container");

signUpButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

signInButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});
