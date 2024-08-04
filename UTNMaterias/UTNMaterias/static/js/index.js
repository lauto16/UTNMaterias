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


function getSubjectState(element) {
    return element.getAttribute('data-state')
}


function getSubjectFromTree(tree, subject_id){
    subject_id = parseInt(subject_id)
    if (subject_id === 0){
        subject_id = 1
    }
    const all_subjects = Object.values(tree).flat()
    for (let i = 0; i < all_subjects.length; i++) {
        const subject = all_subjects[i];
        if(subject.id === subject_id){
            return subject
        }
        
    }
}


function isEnrollable(subject, tree){
    for (let i = 0; i < subject.fathers.length; i++) {
        const father_id = subject.fathers[i];
        const father = getSubjectFromTree(tree, father_id)
        
        // check regularity too...
        if (!father.is_approved) {
            return false
        }
    }
    return true
}


function changeHtmlStates(subject){
    if(subject.id === 1){
        // it's ingreso
        var subject_div = document.getElementById(`subject_${subject.id - 1}_year_0`)
    }

    else{
        var subject_div = document.getElementById(`subject_${subject.id}`)
    }

    if (subject.is_approved) {
        subject_div.setAttribute('data-state', 'approved')
        subject_div.style.backgroundColor = '#bdeda4'   
    }
    else {
        subject_div.setAttribute('data-state', 'null')
        if (subject.is_enrollable){
            subject_div.style.backgroundColor = '#d0d7d9'    
        }
        else{
            subject_div.style.backgroundColor = '#b5dcf7'    
        }
    }
}


function updateTree(tree){

    let all_subjects = Object.values(tree).flat()
    let subject_slots = document.querySelectorAll('.inUse')

    for (let i = 0; i < all_subjects.length; i++) {
        let subject = all_subjects[i]
        
        // check enrollability
        if(isEnrollable(subject, tree)){
            subject.is_enrollable = true
        }
        else{
            subject.is_enrollable = false
            subject.is_approved = false
        }
        // set as enrollable because it has been approved
        if (subject.is_approved){
            subject.is_enrollable = true    
        }


        //change tree colors
        changeHtmlStates(subject)
        
        
    }

    return tree
}


function changeState(element, tree){
    if(element.getAttribute('data-state') == 'null'){
        let element_id = element.id.split('_')[1]
        let subject = getSubjectFromTree(tree, element_id)
        
        if(subject.is_enrollable){
            element.setAttribute('data-state', 'approved')
            element.style.backgroundColor = '#bdeda4'
            subject.is_approved = true
        }
        else{
            console.error(`${subject.name} is not enrollable yet`)
        }

    }
    else if(element.getAttribute('data-state') == 'approved'){
        element.setAttribute('data-state', 'null')
        element.style.backgroundColor = '#b5dcf7'
        let element_id = element.id.split('_')[1]
        let subject = getSubjectFromTree(tree, element_id)
        subject.is_approved = false
    }

    tree = updateTree(tree)
    console.log(tree)
    /*
    poner como aprobadas
    y regulares todas las anteriores necesarias (recursivamente)
    */

    /* 
    recorrer el arbol entero buscando por:
        -materias que puedan ser cursadas (terminado)
        -materias que no puedan ser cursadas (terminado)
    */
}


function setEventListeners(classname1, classname2, tree){

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
            changeState(element, tree)
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
                ingreso = document.getElementById('subject_0_year_0')
                ingreso.className = 'subject ingreso'
                ingreso.setAttribute('data-state', 'null')
            }
        })
    })


    // change the state of the used slots so them can be distingued from unused ones 
    setInUse('subject')
    // sets the background color, border and id of the unused slots so that they are invisible
    changeSubjectStyle('subject', '#eaeaf7', 0)
    // sets onClick event listeners to all inUse elements
    setEventListeners('subject', 'inUse', tree)
}

