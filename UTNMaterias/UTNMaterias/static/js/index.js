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
    return cookieValue;
}


function getSubject(subject_id) {
    /*
    Returns the data of a Subject when subject_id is passed as an argument
    (The data comes from SubjectAPI)

    Usage:
    
    getSubject(13)
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error fetching subject:', error);
    });

    */
    const query = './apis/subjects/' + subject_id.toString();

    let requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken'),
        },
    };

    return fetch(query, requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            throw error; 
        });
}


function getTree(){
    let requestOptions = {

        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken'),
        }, 
        body: JSON.stringify({
            action: 'get_tree'
        })
    };

    fetch(window.location.href, requestOptions)

        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })

        .then(data => {
            console.log(data)
        })

        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

getTree()