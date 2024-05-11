
async function handDeleteCardClick(id) {
    const { deleteFetch } = await import('../../../static/js/fetch.js');
    const response = await deleteFetch(`/communities/update_community/${id}`)()()    
    if (response.ok!=="ok") {
        alert(response.message);
    }else{
        // 页面刷新
        window.location.reload();
    }
}
function handEditCardClick(id) {
    window.location.href = '/communities/editCommunity/' + id;
}
async function handInfoEditClick(element) {
    const info = JSON.parse(element.getAttribute('data-info'));
    const url = `/communities/update_community/${info.id}`;
    const data = { info };
    const response = await getFetch(url)(data)(); // 第三个参数是header，没有就不传
}