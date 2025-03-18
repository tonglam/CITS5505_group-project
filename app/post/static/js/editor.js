const postUrl = "/api/v1/posts/create/post";
const commentUrl = "/api/v1/posts/create/comment";

document.addEventListener("DOMContentLoaded", function () {
  // Quill rich text editor options
  const options = {
    theme: "snow",
    bounds: document.body,
    debug: "warn",
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
          ["link", "image"],
        ],
        handlers: {
          image: function () {
            document.getElementById("image-upload").click();
          },
        },
      },
      clipboard: {
        matchVisual: false,
      },
      imageResize: {
        parchment: Quill.import("parchment"),
        displayStyles: {
          backgroundColor: "black",
          border: "none",
          color: "white",
        },
        modules: ["Resize", "DisplaySize", "Toolbar"],
        overlayStyles: {
          position: "absolute",
          boxSizing: "border-box",
          border: "1px dashed #444",
        },
        handleStyles: {
          backgroundColor: "black",
          border: "none",
          color: "white",
        },
        toolbarStyles: {
          backgroundColor: "black",
          border: "none",
          color: "white",
        },
      },
    },
    placeholder: "Enter content",
    readOnly: false,
  };

  // Initialize Quill editor with custom observer
  const quill = new Quill("#editor-container", options);

  // Use MutationObserver instead of deprecated DOMNodeInserted
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeName === "IMG") {
            // Handle new image insertion
            node.addEventListener("load", () => {
              quill.update();
            });
          }
        });
      }
    });
  });

  // Start observing the editor
  observer.observe(quill.root, {
    childList: true,
    subtree: true,
  });

  // Handle image upload event
  const imageInput = document.getElementById("image-upload");
  imageInput.addEventListener("change", async function () {
    const file = imageInput.files[0];
    try {
      const valid = await handleBeforeUpload(file);
      if (valid) {
        // Create FormData and append file
        const formData = new FormData();
        formData.append("image", file);

        // Upload to R2 using postFetch service
        try {
          const rawResponse = await postFetch("/api/v1/upload/image")(
            formData
          )();

          // Parse the response if it's a Response object
          const response =
            rawResponse instanceof Response
              ? await rawResponse.json()
              : rawResponse;

          // Check if response exists
          if (!response) {
            throw new Error("No response received from server");
          }

          // Handle successful upload - checking both response types
          if (
            response.code === 201 ||
            response.code === 200 ||
            (rawResponse instanceof Response && rawResponse.ok)
          ) {
            // Try to get the image URL from various possible response structures
            const imageUrl =
              response.data?.image_url ||
              response.message?.image_url ||
              response.url;

            if (!imageUrl) {
              console.error("Response structure:", response);
              throw new Error("Could not find image URL in response");
            }

            const length = quill.getSelection()?.index || 0;
            quill.insertEmbed(length, "image", imageUrl);
            quill.setSelection(length + 1);
          } else {
            console.error("Unexpected response:", response);
            const errorMsg =
              response.message ||
              (response.msg
                ? `Server error: ${response.msg}`
                : `Server returned unexpected status: ${
                    response.code || rawResponse.status || "undefined"
                  }`);
            throw new Error(errorMsg);
          }
        } catch (uploadError) {
          console.error("Upload request failed:", uploadError);
          throw new Error(
            uploadError.message || "Failed to process server response"
          );
        }
      }
    } catch (error) {
      console.error("Error details:", error);
      alert(`Error uploading image: ${error.message}`);
    }
  });

  // Check format and size before upload
  function handleBeforeUpload(file) {
    return new Promise((resolve, reject) => {
      const validTypes = [".gif", ".jpg", ".jpeg", ".png"];
      const fileType = file.name.slice(file.name.lastIndexOf("."));
      if (!validTypes.includes(fileType)) {
        alert("Only .gif/.jpg/.jpeg/.png formats are supported!");
        resolve(false);
      } else if (file.size / 1024 / 1024 > 2) {
        // Assume max file size is 2MB
        alert("File size cannot exceed 2MB!");
        resolve(false);
      } else {
        resolve(true);
      }
    });
  }

  const content = document.createElement("input");
  content.setAttribute("type", "hidden");
  content.setAttribute("name", "content");
  content.value = quill.root.innerHTML;
  // this.appendChild(content);
});

async function createPost(title, community, content, tag) {
  const data = {
    title: title,
    community: community,
    content: content,
    tag: tag,
  };

  try {
    const rawResponse = await postFetch(postUrl)(data)();

    // Parse the response if it's a Response object
    const response =
      rawResponse instanceof Response ? await rawResponse.json() : rawResponse;

    if (
      response.code === 201 ||
      (rawResponse instanceof Response && rawResponse.status === 201)
    ) {
      const postId = response.data?.post_id;
      if (postId) {
        window.location.href = "/posts/" + postId;
      } else {
        console.error("Post created but no post_id in response:", response);
        window.location.href = "/";
      }
    } else {
      console.error("Failed to create post:", response);
      alert(
        response.message ||
          `Failed to create post: ${
            response.code || response.status || "Unknown error"
          }`
      );
    }
  } catch (error) {
    console.error("Error creating post:", error);
    alert("Error creating post: " + (error.message || "Unknown error"));
  }
}

async function editPost(title, community, content, tag) {
  const data = {
    title: title,
    community: community,
    content: content,
    tag: tag,
  };

  const response = await putFetch(postUrl)(data)();
  if (response.code == 200) {
    window.location.href = "/posts/" + response.message.post_id;
  } else {
    alert(response.message);
  }
}

async function createComment(content) {
  const data = {
    content: content,
  };

  const response = await postFetch(commentUrl)(data)();
  if (response.code == 201) {
    window.location.href = "/posts/" + response.message.post_id;
  } else {
    alert(response.message);
  }
}

async function editComment(content) {
  const data = {
    content: content,
  };

  const response = await putFetch(commentUrl)(data)();
  if (response.code == 200) {
    window.location.href = "/posts/" + response.message.post_id;
  } else {
    alert(response.message);
  }
}

document
  .getElementById("postForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const mode = document.getElementById("mode").value;
    const title = document.getElementById("postTitle")
      ? document.getElementById("postTitle").value
      : null;
    const community = document.getElementById("postCommunity")
      ? document.getElementById("postCommunity").value
      : null;
    const tag = document.getElementById("postTag")
      ? document.getElementById("postTag").value
      : null;
    const content = document.getElementsByClassName("ql-editor")[0].innerHTML;
    const postId = document.getElementById("postId")
      ? document.getElementById("postId").value
      : null;

    if (mode === "post") {
      createPost(title, community, content, tag);
    } else if (mode === "comment") {
      createComment(content);
    } else if (mode === "edit_comment") {
      editComment(content);
    } else if (mode === "edit_post") {
      editPost(title, community, content, tag);
    }
  });
