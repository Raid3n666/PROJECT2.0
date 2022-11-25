
function like(show_id, user_id){
    fetch(`/api/like/${show_id}`, {
        method : 'POST',
        body : JSON.stringify({'user_id' : Number(user_id)}),
        headers:{'Content-Type' : 'application/json'}
    })
    const button = document.getElementById('l' + show_id)
    const numLikes = button.childNodes[3]
    const img = button.childNodes[1]
    img.src = '../../static/icons/redheart.png'
    numLikes.textContent = Number(numLikes.textContent) + 1
    button.onclick = () => {unlike(show_id, user_id)}
}

function unlike(show_id, user_id) {
    fetch(`/api/like/${show_id}`, {
        method : 'POST',
        body : JSON.stringify({'user_id' : Number(user_id)}),
        headers:{'Content-Type' : 'application/json'}
    })
    const button = document.getElementById('l' + show_id)
    const numLikes = button.childNodes[3]
    const img = button.childNodes[1]
    img.src = '../../static/icons/heart.png'
    numLikes.textContent = Number(numLikes.textContent) - 1
    button.onclick = () => {like(show_id, user_id)}
}

function star(show_id, user_id){
    fetch(`/api/star/${show_id}`, {
        method : 'POST',
        body : JSON.stringify({'user_id' : Number(user_id)}),
        headers:{'Content-Type' : 'application/json'}
    })
    const button = document.getElementById('s' + show_id)
    const img = button.childNodes[1]
    img.src = '../../static/icons/yellowstar.png'
    button.onclick = () => {unstar(show_id, user_id)}
}

function unstar(show_id, user_id){
    fetch(`/api/star/${show_id}`, {
        method : 'POST',
        body : JSON.stringify({'user_id' : Number(user_id)}),
        headers:{'Content-Type' : 'application/json'}
    })
    const button = document.getElementById('s' + show_id)
    const img = button.childNodes[1]
    img.src = '../../static/icons/star.png'
    button.onclick = () => {star(show_id, user_id)}
}

function comment(show_id, user_id) {
    const content = document.getElementById('comment-content').textContent
    fetch(`/api/comment/${show_id}`, {
        method : 'POST',
        body : JSON.stringify({
            'user_id' : user_id,
            'content' : content
        }),
        headers : {'Content-type' : 'application/json'}
    }).then(() => {window.location.reload()}) .then(() => {document.body.scrollTop = document.body.scrollHeight;}) 
    
}

function likeComment(user_id, comment_id) {
    fetch(`/api/likecomment/${comment_id}`, {
        method : 'POST',
        body : JSON.stringify({
            'user_id' : user_id,
        }),
        headers : {'Content-type' : 'application/json'}
    })
    const button = document.getElementById('l'+ comment_id)
    const img = document.getElementById('i'+ comment_id)
    const likeCount = document.getElementById('span' + comment_id)
    console.log({'button' : button, 'img' : img, "likecount" : likeCount})
    likeCount.textContent = Number(likeCount.textContent) + 1
    img.src = '../../static/icons/redheart.png'
    button.onclick = () => {unlikeComment(user_id, comment_id)}

}

function unlikeComment(user_id, comment_id) {
    fetch(`/api/likecomment/${comment_id}`, {
        method : 'POST',
        body : JSON.stringify({
            'user_id' : user_id,
        }),
        headers : {'Content-type' : 'application/json'}
    })
    const button = document.getElementById('l' + comment_id)
    const img = document.getElementById('i'+ comment_id)
    const likeCount = document.getElementById('span' + comment_id)
    console.log(img, button)
    likeCount.textContent = Number(likeCount.textContent) - 1
    img.src = '../../static/icons/heart.png'
    button.onclick = () => {likeComment(user_id, comment_id)}
}

function enableSubmit(){
    const changedInput = document.getElementById('write-comment');
    const btn = document.querySelector('input[type="submit"]');
    let isValid = true;
    if (changedInput.value.trim() === "" || changedInput.value === null){
    isValid = false;
    }
    btn.disabled = !isValid;
    }

function enableSearch(){
    const changedInput = document.querySelector("body > div.search-form > form > input[type=text]:nth-child(1)");
    const btn = document.querySelector("body > div.search-form > form > input[type=submit]:nth-child(2)");
    let isValid = true;
    if (changedInput.value.trim() === "" || changedInput.value === null){
    isValid = false;
    }
    btn.disabled = !isValid;
    }