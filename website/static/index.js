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

// function editNote(noteId){
//     const newNote = prompt("Enter the new note:");
//     if (newNote) {
//         fetch("/edit-note", {
//             method: "POST",
//             body: JSON.stringify({ noteId: noteId, newNote: newNote }),
//         }).then((_res) => {
//             window.location.href = "/";
//         });
//     }
// }