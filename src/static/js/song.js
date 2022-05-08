document.getElementById('song-item-add').addEventListener("click", () => {
    let playlists = document.getElementById('song-item-playlists');

    if (playlists.style.display === "") {
        playlists.style.display = "none";
    } else {
        playlists.style.display = null;
    }
})