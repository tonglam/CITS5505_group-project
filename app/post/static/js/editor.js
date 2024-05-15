const postUrl = "/api/v1/posts/create_post";
const commentUrl = "/api/v1/posts/create_comment"; 


function initializeEditor() {
   var quill = new Quill('#editor-container', {
     theme: 'snow'
   });

/*    var postForm = document.getElementById('postForm');
  var mode = postForm.getAttribute('data-mode');
  var replyContent = postForm.getAttribute('data-reply-content');

  if (mode === 'edit' && replyContent) {
    quill.clipboard.dangerouslyPasteHTML(replyContent);
  } */

   document.getElementById('postForm').onsubmit = function() {
     var content = document.createElement('input');
     content.setAttribute('type', 'hidden');
     content.setAttribute('name', 'content');
     content.value = quill.root.innerHTML;
     this.appendChild(content);
   };
}

document.addEventListener('DOMContentLoaded', initializeEditor);



async function createPost(title, community, content, tag) {
    const data = {
        title: title,
        community: community,
        content: content,
        tag: tag
    };
    console.log(data);


    const response = await postFetch(postUrl)(data)();
    if (response.code == 201) {
      window.location.href = "/posts/" + response.message.post_id;
  } else {
      alert(response.message);
  }
}



async function createComment(content) {
    const data = {
        content: content
    };

    const response = await postFetch(commentUrl)(data)();
    console.log(response.message.post_id)
    console.log(response.code)
    if (response.code == 201) {
        window.location.href = "/posts/" + response.message.post_id;
    } else {
        alert(response.message);
    }
}




document.getElementById('postForm').addEventListener('submit', function(event) {
  event.preventDefault();

  var mode = document.getElementById('mode').value;
  var title = document.getElementById('postTitle') ? document.getElementById('postTitle').value : null; 
  var community = document.getElementById('postCommunity') ? document.getElementById('postCommunity').value : null;
  var tag = document.getElementById('postTag') ? document.getElementById('postTag').value : null;
  var content = document.getElementsByClassName('ql-editor')[0].innerHTML;
  var postId = document.getElementById('postId') ? document.getElementById('postId').value : null;

  if (mode === 'post') {
      createPost(title, community, content, tag);
  } else if (mode === 'comment') {
      createComment(content);
  } 
});