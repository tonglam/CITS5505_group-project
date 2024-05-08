$(document).ready(function () {
  ".count".each(function () {
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
});

const init_tab_switch = (tab_data_name) => {
  // reset render id and url
  document.getElementById("render-id").innerHTML = `users-${tab_data_name}`;
  document.getElementById(
    "render-url"
  ).innerHTML = `/users/lists?name=${tab_data_name}&page=1`;

  // re-render
  re_render({ page: 1 });
};
