function getCookie(name) {

    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log(cookieValue)
    return cookieValue;
}


function sendCareer(career) {
    //Redirects the user to index if career exists

    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken'),
        },
        body: JSON.stringify({
            'career': career
        })
    };

    return fetch('./', requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })

        .then(data => {
            window.location.replace(`${window.location.href}index/${career}`);
        })

        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            throw error; 
        });
}

careers = document.querySelectorAll('.career')
careers.forEach(element => {
    element.addEventListener('click', function(e){
        sendCareer(element.id)
    });
});