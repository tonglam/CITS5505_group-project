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

  const response = await fetch("/api/v1/email_exists/" + email);
  const res = await response.json();
  console.log(res);
}
