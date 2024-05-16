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
  // active tab
  const tabList = [].slice.call(
    document.querySelectorAll('a[data-bs-toggle="tab"]')
  );
  tabList.forEach((tab) => {
    if (tab.id === `tab-nav-${tab_data_name}`) {
      tab.classList.add("tab_active");
      tab.classList.remove("tab_inactive");
    } else {
      tab.classList.add("tab_inactive");
      tab.classList.remove("tab_active");
    }
  });

  // reset render id and url
  document.getElementById("render-id").innerHTML = `users-${tab_data_name}`;
  document.getElementById(
    "render-url"
  ).innerHTML = `/users/lists?name=${tab_data_name}&page=1`;

  // re-render
  re_render({ page: 1 });
};
