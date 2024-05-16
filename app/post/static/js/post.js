const postUrl = "/api/v1/posts/create_post";
const commentUrl = "/api/v1/posts/create_comment";


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
  console.log("Sending request to:", url, "with data:", data);

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
      alert(`${actionType.charAt(0).toUpperCase() + actionType.slice(1)} successful for request ID ${requestId} replyID ${replyId}`);
      break;
    case `un${actionType} success`:
      userStatus[statusKey][requestId][replyKey] = false;
      alert(`Un${actionType} successful for request ID ${requestId} replyID ${replyId}`);
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
    console.error("Error details:", error);
  }
}

window.toggleLike = (requestId, replyId) => toggleAction(requestId, replyId, 'like');
window.toggleSave = (requestId, replyId) => toggleAction(requestId, replyId, 'save');



async function deletePost(postId) {
  const data = {
    post_id: postId
  };
  const response = await deleteFetch(postUrl)(data)();
  console.log(response)
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
  console.log(response)

}

document.getElementById('deletePostButton').addEventListener('click', function(event) {
  event.preventDefault();

  var postId = this.getAttribute('data-post-id');
  deletePost(postId);
  
});

var deleteButtons = document.getElementsByClassName('btn-delete-reply');

for (var i = 0; i < deleteButtons.length; i++) {
  deleteButtons[i].addEventListener('click', function(event) {
    event.preventDefault();
    var replyId = this.getAttribute('data-reply-id');
    var postId = this.getAttribute('data-post-id');
    deleteComment(postId, replyId).then(() => {
      window.location.reload();
    }).catch((error) => {
      console.error('Error deleting comment:', error);
    });;
  });
}


// for set the initial status

document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Fetch user likes
    const likesResponse = await getFetch('/api/user/likes')()();
    initializeLikes(likesResponse.user_likes);

    // Fetch user saves
    const savesResponse = await getFetch('/api/user/saves');
    const savesData = await savesResponse.json();
    initializeSaves(savesData.user_saves);
  } catch (error) {
    console.error("Error fetching likes or saves:", error);
  }
});