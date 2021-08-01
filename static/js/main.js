setTimeout(function(){
    document.getElementById("message").innerHTML = '';
}, 4000);


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
         }
        }
    }
    return cookieValue;
}


function DeleteBook(book_id) {
    let result = confirm('Are you sure you want to delete this entry?');
    if (result) {

    const csrftoken = getCookie('csrftoken');

    fetch('/api/books/' + book_id, {
        method: 'DELETE',
        headers: {
                    'Content-Type':'application/json',
                    'X-CSRFTOKEN': csrftoken
                },
    }).then(response => response)
        .then(data => {
            location.reload();
        })
        .catch(error => {
            console.log(error)
        })
    }
}