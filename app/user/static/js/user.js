// $(document).ready(function () {
//   // Add click event handler for the radio button
//   $("#tab-posts").on("click", function () {
//     // Your code to execute when the radio button is clicked
//     console.log("Radio button clicked");
//   });
// });

// init_tab_pagination = () => {
//   reset_tab_pagination("tab-posts", "user-posts", "/users/posts");
//   reset_tab_pagination("tab-likes", "users-likes", "/users/likes");
//   reset_tab_pagination(
//     "tab-label-histories",
//     "users-histories",
//     "/users/histories"
//   );
//   reset_tab_pagination("tab-label-wishes", "users-wishes", "/users/wishes");
// };

// reset_tab_pagination = (id, render_id, render_url) => {
//   console.log("reset tab pagination");
//   console.log("id:", id);
//   console.log("render_id:", render_id);
//   console.log("render_url:", render_url);

//   document.getElementById(id).addEventListener("click", function () {
//     console.log("click tab");
//     // reset render id and url
//     document.getElementById("render-id").innerHTML = render_id;
//     document.getElementById("render-url").innerHTML = render_url;
//     // re-render
//     re_render({ page: 1 });
//   });
// };

// for user data container
$(".count").each(function () {
  $(this)
    .prop("Counter", 0)
    .animate(
      {
        Counter: $(this).text(),
      },
      {
        duration: 1500,
        easing: "linear",
        step: function (now) {
          $(this).text(Math.ceil(now));
        },
      }
    );
});
