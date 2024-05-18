const postUrl = "/api/v1/posts/create/post";
const commentUrl = "/api/v1/posts/create/comment"; 


document.addEventListener('DOMContentLoaded', function() {
  // Quill rich text editor options
  const options = {
    theme: 'snow',
    bounds: document.body,
    debug: 'warn',
    modules: {
      toolbar: {
        container: [
          ["bold", "italic", "underline", "strike"],
          ["blockquote", "code-block"],
          [{ list: "ordered" }, { list: "bullet" }],
          [{ indent: "-1" }, { indent: "+1" }],
          [{ size: ["small", false, "large", "huge"] }],
          [{ header: [1, 2, 3, 4, 5, 6, false] }],
          [{ color: [] }, { background: [] }],
          [{ align: [] }],
          ["clean"],
          ["link", "image"]
        ],
      },
      imageResize: {
        displayStyles: {
          backgroundColor: 'black',
          border: 'none',
          color: 'white'
        },
        modules: ['Resize', 'DisplaySize', 'Toolbar']
      }
    },
    placeholder: 'Enter content',
    readOnly: false,
  };

  // Initialize Quill editor
  const quill = new Quill('#editor-container', options);

  // Handle image upload event
  const imageInput = document.getElementById('image-upload');
  quill.getModule('toolbar').addHandler('image', function() {
    imageInput.click();
  });

  imageInput.addEventListener('change', function() {
    const file = imageInput.files[0];
    handleBeforeUpload(file).then(valid => {
      if (valid) {
        const reader = new FileReader();
        reader.onload = function(e) {
          const base64Image = e.target.result;
          insertImage(base64Image);
        };
        reader.readAsDataURL(file);
      }
    });
  });

  // Check format and size before upload
  function handleBeforeUpload(file) {
    return new Promise((resolve, reject) => {
      const validTypes = ['.gif', '.jpg', '.jpeg', '.png'];
      const fileType = file.name.slice(file.name.lastIndexOf('.'));
      if (!validTypes.includes(fileType)) {
        alert('Only .gif/.jpg/.jpeg/.png formats are supported!');
        resolve(false);
      } else if (file.size / 1024 / 1024 > 2) { // Assume max file size is 2MB
        alert('File size cannot exceed 2MB!');
        resolve(false);
      } else {
        resolve(true);
      }
    });
  }

  // Insert image into the editor
  function insertImage(base64Image) {
    const length = quill.getSelection().index;
    quill.insertEmbed(length, 'image', base64Image);
    quill.setSelection(length + 1);
  }

  var content = document.createElement('input');
  content.setAttribute('type', 'hidden');
  content.setAttribute('name', 'content');
  content.value = quill.root.innerHTML;
  this.appendChild(content);

});


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


async function editPost(title, community, content, tag) {
  const data = {
      title: title,
      community: community,
      content: content,
      tag: tag
  };
  console.log(data);


  const response = await putFetch(postUrl)(data)();
  if (response.code == 200) {
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


async function editComment(content) {
  const data = {

      content: content
  };

  const response = await putFetch(commentUrl)(data)();
  console.log(response.message.post_id)
  console.log(response.code)
  if (response.code == 200) {
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
  } else if (mode === 'edit_comment'){
      editComment(content);
  } else if (mode === 'edit_post'){
      editPost(title, community, content, tag);
  }
});