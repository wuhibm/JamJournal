document.addEventListener('DOMContentLoaded', () => {
    let delete_buttons = document.querySelectorAll(".delete");
    delete_buttons.forEach(delete_button => delete_button.addEventListener('click', () => { delete_review(delete_button.parentElement.parentElement.parentElement) }));
    let edit_buttons = document.querySelectorAll(".edit");
    edit_buttons.forEach(edit_button => edit_button.addEventListener('click', () => { edit_review(edit_button.parentElement.parentElement.parentElement) }));
    let reply_buttons = document.querySelectorAll(".reply");
    reply_buttons.forEach(reply_button => reply_button.addEventListener('click', () => { reply_to_review(reply_button.parentElement.parentElement.parentElement) }));
    let like_buttons = document.querySelectorAll(".like");
    like_buttons.forEach(element => element.addEventListener("click", () => toggle_like(element)));

    fetch("/liked_reviews")
        .then(response => response.json())
        .then(likes => {
            likes.forEach(like => {
                let liked = document.querySelector(`#like-button${like}`);
                if (liked != null) {
                    liked.classList.add("liked");
                    liked.classList.remove("unliked");
                }
            })
        })
});


function edit_review(review) {
    let reviewId = review.id;
    window.location.replace(`/edit/${reviewId}`);
}

function delete_review(review) {

    let reviewId = review.id;
    fetch(`/delete/${reviewId}`)
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                alert("ERROR: You cannot delete other people's reviews");
            }
            else {
                review.remove();
            }
        })
}

function reply_to_review(review) {
    let reviewId = review.id;
    window.location.replace(`/view_review/${reviewId}`);
}

function toggle_like(button) {
    button.classList.toggle("liked");
    button.classList.toggle("unliked");
    let reviewId = button.dataset.review;
    console.log(button.dataset);
    console.log(reviewId);
    fetch('/like', {
        method: "POST",
        body: JSON.stringify({
            id: reviewId
        })
    })
        .then(() => {
            fetch("/likes/" + reviewId)
                .then(response => response.json())
                .then(result => {
                    //document.querySelector(`#likes${reviewId}`).innerHTML = result.likes + ( " likes");
                    document.querySelector(`#likes${reviewId}`).innerHTML = result.likes == 1 ? result.likes + (" like") : result.likes + (" likes");
                });
        })
        .then(() => {
            button.blur();
        });
}