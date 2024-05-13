document.addEventListener("DOMContentLoaded", function () {
  const submitBtn = document.getElementById("submitBtn");
  const nameInput = document.getElementById("name");
  const descriptionInput = document.getElementById("description");
  const categoryIdSelect = document.getElementById("category_id");
  const csrf_token = document.getElementById("csrf_token");
  // Listen for form submission events
  submitBtn.addEventListener("click", async function (event) {
    event.preventDefault(); // Prevent form from submitting by default
    const { postFetch } = await import("../../../static/js/fetch.js");

    // Manually collect form data

    const postDataObj = {
      name: nameInput.value,
      description: descriptionInput.value,
      category_id: categoryIdSelect.value,
      csrf_token: csrf_token.value,
    };
    //Convert ordinary object to FormData instance
    const postData = new FormData();
    for (let key in postDataObj) {
      postData.append(key, postDataObj[key]);
    }
    // Send POST request using postFetch
    const response = await postFetch(
      "{% if record_entity %}{{ url_for('community.update_community', community_id=record_entity.id) }}{% else %}{{ url_for('community.add_community') }}{% endif %}"
    )(postData)({});
    if (response.ok === "ok") {
      // Handle successful responses such as redirects or prompts
      alert(response.message);
      window.location.href = "/communities/";
    } else {
      //Handling error responses
      alert(response.message);
    }
  });
});

async function handDeleteCardClick(id) {
  const { deleteFetch } = await import("../../../static/js/fetch.js");
  const response = await deleteFetch(`/communities/update_community/${id}`)()();
  if (response.ok !== "ok") {
    alert(response.message);
  } else {
    // page update
    window.location.reload();
  }
}
function handEditCardClick(id) {
  window.location.href = "/communities/editCommunity/" + id;
}
