function toggleReplies(button, className) {
  const elements = document.getElementsByClassName(className);
  if (elements.length > 0) {
    const element = elements[0];
    if (element.classList.contains("hidden")) {
      element.classList.remove("hidden");
      button.textContent = "Collapse All";
    } else {
      element.classList.add("hidden");
      button.textContent = "Show Replies";
    }
  }
}

function toggleTextExpansion() {
  const text = document.querySelector(".card-text");
  const button = document.querySelector(".expand-button");
  if (text.classList.contains("expanded")) {
    text.classList.remove("expanded");
    button.textContent = "Show More";
  } else {
    text.classList.add("expanded");
    button.textContent = "Show Less";
  }
}

function toggleLike() {}

function toggleSave() {}
