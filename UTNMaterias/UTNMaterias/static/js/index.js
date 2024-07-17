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


/* REEMPLAZAR CON CONSULTA CON API
function getSubject(subject_id) {

    let requestOptions = {

        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken'),
        },
        // send 
        body: JSON.stringify({
            action: 'getSubject',
            subject_id: subject_id
        })
    };

    fetch('./', requestOptions)

        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })

        .then(data => {
            if (data.success === true)
                console.log(data)
            else{
                //errorHandler(error=data.error)
                console.log('error')
            }
            })

        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });

}
*/