document.addEventListener('DOMContentLoaded', () => {
    load_home();
});

function load_home(){
    fetch('/featured')
    .then(response => response.json())
    .then(result => {
        let albums = result.albums.items;
        for(let i = 0; i < albums.length; i++){
            console.log(albums[i].name);
        }
    });
}