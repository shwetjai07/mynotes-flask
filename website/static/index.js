function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST", body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}


function editNote(noteId) {

    window.location.href = `/edit-note?noteId=${noteId}`;

}

function sendToContact(){

    window.location.href = `/contact-us`;
}

function sendToAdmin(){

    window.location.href = `/admin-panel`;
}