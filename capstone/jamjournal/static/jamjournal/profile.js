document.addEventListener('DOMContentLoaded', () => {
    let button = document.querySelector("#follow");
    if (button != null){
        button.addEventListener('click', () => toggle_follow(button));
    }
});


function toggle_follow(button){

    let target_user_id = window.location.href.slice(window.location.href.lastIndexOf('/')+1)
    // fetch('/user')
    // .then(response => response.json())
    // .then(result => {
    //     current_user_id = result.user;
    //     fetch('/follow', {
    //         method: "POST",
    //         body: JSON.stringify({
    //             id1: current_user_id,
    //             id2: target_user_id
    //         })
    //     })
    //     .then(() => {
    //         fetch('/follows/' + target_user_id)
    //         .then( res => res.json())
    //         .then( out => {
    //             document.querySelector("#followers").innerHTML = out.followers + " Followers";
    //             document.querySelector("#following").innerHTML = out.following + " Following";
    //         } );
    //     })
    //     .then(() => button.innerHTML = button.innerHTML.trim() === "Follow" ? "Unfollow" : "Follow");
    // });
    fetch(`/follow/${target_user_id}`)
    .then(() => {
        fetch('/follows/' + target_user_id)
        .then( res => res.json())
        .then( out => {
            document.querySelector("#followers").innerHTML = "Followers: " + out.followers;
            document.querySelector("#following").innerHTML = "Following: " +out.following;
        } );
    })
    .then(() => button.innerHTML = button.innerHTML.trim() === "Follow" ? "Unfollow" : "Follow");


}

