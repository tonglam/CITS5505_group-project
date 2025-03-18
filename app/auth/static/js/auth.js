$(document).ready(function () {
  // sign in and sign up
  const signUpButton = document.getElementById("signUpSubmitSm");
  const signInButton = document.getElementById("signIn");
  const container = document.getElementById("login_container_lg");

  if (signUpButton !== null && container !== null) {
    signUpButton.addEventListener("click", () => {
      container.classList.add("right-panel-active");
    });
  }

  if (signInButton !== null && container !== null) {
    signInButton.addEventListener("click", () => {
      container.classList.remove("right-panel-active");
    });
  }

  // forgot password page - return to login
  const forgotReturnDiv = document.getElementById("forgotReturn");

  if (forgotReturnDiv !== null) {
    forgotReturnDiv.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "/auth/auth";
    });
  }

  $("#email").on("blur", function () {
    checkEmail(this.value);
  });
});

async function checkEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
