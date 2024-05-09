function initializeEditor() {
   var quill = new Quill('#editor-container', {
     theme: 'snow'
   });

   document.getElementById('postForm').onsubmit = function() {
     var content = document.createElement('input');
     content.setAttribute('type', 'hidden');
     content.setAttribute('name', 'content');
     content.value = quill.root.innerHTML;
     this.appendChild(content);
   };
}

document.addEventListener('DOMContentLoaded', initializeEditor);
