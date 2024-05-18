const postUrl = "/api/v1/posts/create/post";
const commentUrl = "/api/v1/posts/create/comment";


function toggleReplies(button, className) {
  const elements = document.getElementsByClassName(className);
  if (elements.length > 0) {
    const firstElement = elements[0];
    if (firstElement.classList.contains("hidden")) {
      for (let i = 0; i < elements.length; i++) {
        elements[i].classList.remove("hidden");
      }
      button.textContent = "Collapse All";
    } else {
      for (let i = 0; i < elements.length; i++) {
        elements[i].classList.add("hidden");
      }
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

const apiUrlBase = '/api/v1/users/';
let userStatus = {
  likes: {},
  saves: {}
};

async function sendRequest(requestId, replyId, actionType, method) {
  const data = {
    request_id: requestId,
    reply_id: replyId
  };

  const url = `${apiUrlBase}${actionType}s`;

  const response = await (method === 'POST' ? postFetch : deleteFetch)(url)(data)();
  return response;
}

function handleResponse(response, requestId, replyId, actionType) {
  const statusKey = actionType === 'like' ? 'likes' : 'saves';

  if (!userStatus[statusKey][requestId]) {
    userStatus[statusKey][requestId] = {};
  }

  const replyKey = replyId || 'no-reply';

  switch (response.message) {
    case `${actionType} success`:
    case `${actionType} already exists`:
      userStatus[statusKey][requestId][replyKey] = true;
      break;
    case `un${actionType} success`:
      userStatus[statusKey][requestId][replyKey] = false;
      break;
    default:
      alert('Unexpected error occurred.');
      break;
  }
  updateButtonStyle(requestId, replyKey, actionType);
}

function updateButtonStyle(requestId, replyKey, actionType) {
  const button = document.getElementById(`${actionType}-button-${replyKey}`);
  const isActioned = userStatus[actionType === 'like' ? 'likes' : 'saves'][requestId][replyKey];
  button.innerHTML = isActioned ? `Un${actionType}` : actionType.charAt(0).toUpperCase() + actionType.slice(1);
  button.classList.toggle('actioned', isActioned);
  if (actionType === 'like') {
    button.style.color = isActioned ? 'red' : '';
  } else if (actionType === 'save') {
    button.style.color = isActioned ? 'blue' : '';
  }
}

async function toggleAction(requestId, replyId, actionType) {
  const statusKey = actionType === 'like' ? 'likes' : 'saves';
  let isActioned;

  if (!userStatus[statusKey][requestId]) {
    userStatus[statusKey][requestId] = {};
  }

  const replyKey = replyId || 'no-reply';
  isActioned = userStatus[statusKey][requestId][replyKey];

  const method = isActioned ? 'DELETE' : 'POST';
  try {
    const response = await sendRequest(requestId, replyId, actionType, method);
    handleResponse(response, requestId, replyId, actionType);
  } catch (error) {
    alert(`An internet issue occurred while toggling the ${actionType}. Please try again.`);
  }
}

window.toggleLike = (requestId, replyId) => toggleAction(requestId, replyId, 'like');
window.toggleSave = (requestId, replyId) => toggleAction(requestId, replyId, 'save');

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const likeButtons = document.querySelectorAll('.btn-like, .btn-like-reply');

    likeButtons.forEach(button => {
      const requestId = button.getAttribute('data-request-id');
      const replyId = button.getAttribute('data-reply-id') || 'no-reply';

      if (!userStatus.likes[requestId]) {
        userStatus.likes[requestId] = {};
      }

      if (button.classList.contains('liked')) {
        button.innerHTML = 'Unlike';
        button.style.color = 'red';
        userStatus.likes[requestId][replyId] = true;
      } else {
        button.innerHTML = 'Like';
        userStatus.likes[requestId][replyId] = false;
      }
    });

    const saveButtons = document.querySelectorAll('.btn-save, .btn-save-reply');

    saveButtons.forEach(button => {
      const requestId = button.getAttribute('data-request-id');
      const replyId = button.getAttribute('data-reply-id') || 'no-reply';

      if (!userStatus.saves[requestId]) {
        userStatus.saves[requestId] = {};
      }

      if (button.classList.contains('saved')) {
        button.innerHTML = 'Unsave';
        button.style.color = 'blue';
        userStatus.saves[requestId][replyId] = true;
      } else {
        button.innerHTML = 'Save';
        userStatus.saves[requestId][replyId] = false;
      }
    });
  } catch (error) {
    console.error("Error initializing like or save buttons:", error);
  }
});


async function deletePost(postId) {
  const data = {
    post_id: postId
  };
  const response = await deleteFetch(postUrl)(data)();
  if (response.code == 200) {
      window.location.href = "/";
  } else {
      alert(response.message);
  }
}


async function deleteComment(postId,replyId) {
  const data = {
    post_id: postId,
    reply_id: replyId
  };
  const response = await deleteFetch(commentUrl)(data)();

}



var deleteButtons = document.getElementsByClassName('btn-delete-reply');

for (var i = 0; i < deleteButtons.length; i++) {
  deleteButtons[i].addEventListener('click', function(event) {
    event.preventDefault();
    var replyId = this.getAttribute('data-reply-id');
    var postId = this.getAttribute('data-post-id');
    deleteComment(postId, replyId).then(() => {
      window.location.reload();
    }).catch((error) => {
    });;
  });
}

var deletePostButton = document.getElementById('deletePostButton');
if (deletePostButton) {
  deletePostButton.addEventListener('click', function(event) {
    event.preventDefault();

    var postId = this.getAttribute('data-post-id');
    deletePost(postId);
  });
}

