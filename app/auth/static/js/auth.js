import { getFetch } from "../../../static/js/fetch.js";

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

  getFetch("/api/v1/auth/email_exists")({ email: email })().then((res) =>
    console.log("GET response:", res),
  );
}
