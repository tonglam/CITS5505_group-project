// getFetch
console.log(11111)

function handDeleteCardClick(element) {
    var info = JSON.parse(element.getAttribute('data-info'));
    console.log(info);
    // 发起DELETE请求到Python后端的删除接口
    fetch(`/communities/delete_community/${info.id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            // 如果后端接口需要身份验证或其他头部信息，这里添加
            // 'Authorization': 'Bearer ' + yourTokenVariable
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log('社区删除成功');
            // 页面刷新
            window.location.reload();
            // 这里可以根据需要处理成功的回调，比如刷新页面或更新UI
        })
        .catch(error => {
            console.error('删除社区时发生错误:', error);
                        // 这里处理错误情况
        });
}