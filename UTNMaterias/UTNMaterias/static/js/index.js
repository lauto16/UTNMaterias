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


function getTree(career){
    let requestOptions = {

        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken'),
        }
    };

    fetch(`${window.location.origin}/tree_api/tree/career/${career}`, requestOptions)

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


function generateTree(subjects){
    // length = subjects.length() + 6
    const length = 66
    const container = document.getElementById('grid-container')

    // generar los slots del grid
    let year = 0
    for (let i = 0; i < 66; i++) {

        if(i % 11 == 0){
            year += 1
            new_descriptor = document.createElement('div')
            new_descriptor.setAttribute('class', 'descriptor')
            new_descriptor.textContent = 'Año: ' + year.toString()
            container.appendChild(new_descriptor)
        }
        else{
            new_slot = document.createElement('div')
            new_slot.setAttribute('class', 'subject')
            container.appendChild(new_slot)
        }
    }

}

generateTree()

/*

    <div class="subject">
        <p class="subject-name">
            Analisis matem&aacute;tico
        </p>
    </div>
    <div class="subject">
        <p class="subject-name">
            F&iacute;sica 1
        </p>
    </div>
    <div class="subject">
        <p class="subject-name">
            &Aacute;lgebra y geometria anal&iacute;tica
        </p>
    </div>

*/