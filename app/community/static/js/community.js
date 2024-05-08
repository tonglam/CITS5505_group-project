// getFetch
console.log(11111)

function handDeleteCardClick(element) {
    var info = JSON.parse(element.getAttribute('data-info'));
    console.log(info);
    // Initiate a DELETE request to the deletion interface of the Python backend
    fetch(`/communities/update_community/${info.id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            // If the backend interface requires authentication or other headers, add them here
            // 'Authorization': 'Bearer ' + yourTokenVariable
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log('Community deleted successfully');
            // Page refresh
            window.location.reload();
            // Here you can handle successful callbacks as needed, such as refreshing the page or updating the UI
        })
        .catch(error => {
            console.error('An error occurred while deleting the community:', error);
            // Handle error conditions here
        });
}
function handEditCardClick(element) {
    var info = JSON.parse(element.getAttribute('data-info'));
    console.log(info);
    window.location.href = '/communities/editCommunity/'+info.id;
}
async function handInfoEditClick(element) {
    var info = JSON.parse(element.getAttribute('data-info'));
    console.log(info);
    const url = `/communities/update_community/${info.id}`;
    const data = {info};
    const response = await getFetch(url)(data)(); // The third parameter is header, if not, it will not be passed.
    console.log(response);
}