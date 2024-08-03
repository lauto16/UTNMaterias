function getCookie(name) {

    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}


function getSubject(subject_id) {
    /*
    Usage:
    
            getSubject(element.id.split('_')[1])
            .then(data => {
                console.log(data)
            })
            .catch(error => {
                console.error('Error fetching subject:', error)
            })

    */
    const query = `${window.location.origin}/subject_api/subjects/${subject_id.toString()}`
    let requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken'),
        },
    }

    return fetch(query, requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw new Error('Network response was not ok.')
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error)
            throw error 
        })
}


function getTree(career){
    let requestOptions = {

        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken'),
        }
    }

    fetch(`${window.location.origin}/tree_api/tree/career/${career}`, requestOptions)

        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw new Error('Network response was not ok.')
        })

        .then(data => {
            console.log(data)
            generateTree(data)
        })

        .catch(error => {
            console.error('There was a problem with the fetch operation:', error)
        })
}


function changeSubjectStyle(classname, color, border){
    elements = document.querySelectorAll(`.${classname}`)
    elements.forEach(element => {
        if(element.textContent.length == 0){
            element.style.backgroundColor = color
            element.style.border = border
            element.id = ''
        }
    })
}


function setInUse(classname){
    elements = document.querySelectorAll(`.${classname}`)
    elements.forEach(element => {
        if (element.textContent.length > 0) {
            element.className = element.className + ' inUse'
            element.setAttribute('data-state', 'null')
        }
    })
}


function changeState(element){
    if(element.getAttribute('data-state') == 'null'){
        element.setAttribute('data-state', 'approved')
        element.style.backgroundColor = '#bdeda4'
    }
    else if(element.getAttribute('data-state') == 'approved'){
        element.setAttribute('data-state', 'null')
        element.style.backgroundColor = '#b5dcf7'
    }
}


function setEventListeners(classname1, classname2){

    //  all subjects
    elements = document.querySelectorAll(`.${classname1}`)
    let in_use = []
    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        if(element.className.includes(classname2)){
            in_use.push(element)
        }
    }
    in_use.forEach(element => {
        element.addEventListener('click', function(e){
            changeState(element)
        })
    })
}


function generateTree(tree) {
    const container = document.getElementById('grid-container')
    const years = Object.values(tree)
    let yearCounter = 0

    // generate grid
    for (let i = 0; i < 66; i++) {
        if (i % 11 === 0) {
            yearCounter++
            const descriptor = document.createElement('div')
            descriptor.className = 'descriptor'
            descriptor.textContent = `Año: ${yearCounter}`
            container.appendChild(descriptor)
        } else {
            const id = `subject_${i - 11 * yearCounter + 10}_year_${yearCounter}`
            const subjectSlot = document.createElement('div')
            subjectSlot.className = 'subject subject_style'
            subjectSlot.id = id
            container.appendChild(subjectSlot)
        }
    }

    // get all the subjects slots
    const subjectsDivs = document.querySelectorAll('.subject')

    subjectsDivs.forEach(subjectDiv => {
        // get the year by splitting the div's id 
        const year = parseInt(subjectDiv.id.split('_').pop(), 10)
        const yearSubjects = years[year - 1]

        yearSubjects.forEach((subject, index) => {
            // if year == 1 then it's ingreso
            if (year !== 1) {
                const newId = `subject_${index}_year_${year - 1}`
                const subjectElement = document.getElementById(newId)
                if (subjectElement) {
                    subjectElement.textContent = subject.name
                    subjectElement.id = `subject_${subject.id}`
                }
            }
            // it's ingreso
            else{
                document.getElementById('subject_0_year_0').className = 'subject ingreso inUse'
            }
        })
    })


    // change the state of the used slots so them can be distingued from unused ones 
    setInUse('subject')
    // sets the background color, border and id of the unused slots so that they are invisible
    changeSubjectStyle('subject', '#eaeaf7', 0)
    // sets onClick event listeners to all inUse elements
    setEventListeners('subject', 'inUse')
}


