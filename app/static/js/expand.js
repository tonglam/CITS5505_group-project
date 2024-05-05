function toggleReplies(button, className) {
   var elements = document.getElementsByClassName(className);
   if (elements.length > 0) {
       var element = elements[0];
       if (element.classList.contains('hidden')) {
           element.classList.remove('hidden');
           button.textContent = "Collapse All";
       } else {
           element.classList.add('hidden');
           button.textContent = "Show Replies";
       }
   }
}

function toggleTextExpansion() {
   var text = document.querySelector('.card-text');
   var button = document.querySelector('.expand-button');
   if (text.classList.contains('expanded')) {
       text.classList.remove('expanded');
       button.textContent = 'Show More';
   } else {
       text.classList.add('expanded');
       button.textContent = 'Show Less';
   }
}
