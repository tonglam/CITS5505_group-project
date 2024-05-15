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

async function sendRequest(requestId, actionType, method) {
  const url = `${apiUrlBase}${actionType}s/${requestId}`;
  const response = await (method === 'POST' ? postFetch : deleteFetch)(url)({})();
  return response;
}

function handleResponse(response, requestId, actionType) {
    const statusKey = actionType === 'like' ? 'likes' : 'saves';
    switch (response.message) {
        case `${actionType} success`:
        case `${actionType} already exists`:
            userStatus[statusKey][requestId] = true;
            alert(`${actionType.charAt(0).toUpperCase() + actionType.slice(1)} successful for request ID ${requestId}`);
            updateButtonStyle(requestId, actionType);
            break;
        case `un${actionType} success`:
            userStatus[statusKey][requestId] = false;
            alert(`Un${actionType} successful for request ID ${requestId}`);
            updateButtonStyle(requestId, actionType);
            break;
        default:
            alert('Unexpected error occurred.');
            break;
    }
}

function updateButtonStyle(requestId, actionType) {
  const button = document.getElementById(`${actionType}-button`);
  const isActioned = userStatus[actionType === 'like' ? 'likes' : 'saves'][requestId];
  button.innerHTML = isActioned ? `Un${actionType}` : actionType.charAt(0).toUpperCase() + actionType.slice(1);
  button.classList.toggle('actioned', isActioned);
}

async function toggleAction(requestId, actionType) {
    
    const statusKey = actionType === 'like' ? 'likes' : 'saves';
    const isActioned = userStatus[statusKey][requestId];
    const method = isActioned ? 'DELETE' : 'POST';
    try {
        const response = await sendRequest(requestId, actionType, method);
        handleResponse(response, requestId, actionType);
    } catch (error) {
        console.error(`Error sending toggle ${actionType} request:`, error);
        alert(`An internet issue occurred while toggling the ${actionType}. Please try again.`);
    }
}

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

window.toggleLike = (requestId) => toggleAction(requestId, 'like');
window.toggleSave = (requestId) => toggleAction(requestId, 'save');


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