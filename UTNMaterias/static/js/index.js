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


function getSubject(subject_id, career) {
    /*
    Devuelve informacion del subject con id = subject_id (argumento), consultando a la API
    Uso:
    
            getSubject(element.id.split('_')[1], 'sistemas')
            .then(data => {
                console.log(data)
            })
            .catch(error => {
                console.error('Error fetching subject:', error)
            })

    */
    const query = `${window.location.origin}/subject_api/subjects/${career}/${subject_id.toString()}`
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
    // envia una peticion a la API y hace el llamado de generateTree() pasando ambos arboles (regular y approved)
    // como parametros

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
            console.log('APPROVAL_TREE: ', data.approval)
            console.log('REGULAR_TREE: ', data.regular)
            generateTree(data.approval, data.regular, career)
        })

        .catch(error => {
            console.error('There was a problem with the fetch operation:', error)
        })
}


function changeSubjectStyle(classname, color, border, id){
    // cambia el color, borde y id de todos los elementos con clase = classname (argumento) 
    elements = document.querySelectorAll(`.${classname}`)
    elements.forEach(element => {
        if(element.textContent.length == 0){
            element.style.backgroundColor = color
            element.style.border = border
            element.id = id
        }
    })
}


function setInUse(classname){
    // Le agrega la clase inUse a los elementos con clase = classname (argumento)
    elements = document.querySelectorAll(`.${classname}`)
    elements.forEach(element => {
        if (element.textContent.length > 0) {
            element.className = element.className + ' inUse'
            element.setAttribute('data-state', 'null')
        }
    })
}


function getSubjectState(element) {
    // retorna el 'data-state' del elemento html enviado como parametro
    return element.getAttribute('data-state')
}


function getSubjectFromTree(tree, subject_id){
    // busca un subject por su id en un arbol que se pase como parametro
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


function isEnrollable(approval_subject, regular_subject, approval_tree, regular_tree){
    // devuelve true si encuentra:
    //      - un padre de aprobacion que no este aprobado
    //      - un padre de regularidad que no este regular 

    // aprobacion
    for (let i = 0; i < approval_subject.fathers.length; i++) {
        const father_id = approval_subject.fathers[i];
        const father = getSubjectFromTree(approval_tree, father_id)
        
        if (!father.is_approved) {
            return false
        }
    }

    // regularidad
    for (let i = 0; i < regular_subject.fathers.length; i++) {
        const father_id = regular_subject.fathers[i];
        const father = getSubjectFromTree(regular_tree, father_id)
        
        if (!father.is_regular) {
            return false
        }
    }

    return true
}

function isApprovable(approval_subject, regular_subject, approval_tree, regular_tree){
    // a la hora de aprobar una materia, esta tiene que:
    // ser enrollable, tener aprobados los padres de aprobacion y tener aprobados los padres de regularidad
    if (isEnrollable(approval_subject, regular_subject, approval_tree, regular_tree)){
        
        for (let i = 0; i < regular_subject.fathers.length; i++) {
            const father_id = regular_subject.fathers[i];
            const approved_father = getSubjectFromTree(approval_tree, father_id)
            
            if (!approved_father.is_approved) {
                return false
            }
        }
        return true
    }
    else{
        return false
    }
}


function changeHtmlStates(approval_tree, regular_tree){
    let all_approval_subjects = Object.values(approval_tree).flat()
    for (let i = 0; i < all_approval_subjects.length; i++) {
        let approval_subject = all_approval_subjects[i]
        let regular_subject = getSubjectFromTree(regular_tree, approval_subject.id)
        let element = null

        if(approval_subject.id === 1){
            element = document.getElementById('subject_0_year_0')
        }
        else{
            element = document.getElementById(`subject_${approval_subject.id}`)
        }
        
        // approved
        if (approval_subject.is_approved){
            element.setAttribute('data-state', 'approved')
            element.style.backgroundColor = '#d0f2b1'
        }

        // regular
        
        else if(regular_subject.is_regular){
            element.setAttribute('data-state', 'regular')
            element.style.backgroundColor = '#eddcad'
        }

        // null
        else{
            // it's enrollable
            if (isEnrollable(approval_subject, regular_subject, approval_tree, regular_tree)){
                element.style.backgroundColor = '#e1e5ed'
            }
            else{
                element.style.backgroundColor = '#b5dcf7'
            }
            element.setAttribute('data-state', 'null')
        }

    }
}


function updateTrees(approval_tree, regular_tree, career){
    // actualiza el estado de los arboles segun lo que se cambio en changeStates chequeando antes si es posible
    let all_approval_subjects = Object.values(approval_tree).flat()

    for (let i = 0; i < all_approval_subjects.length; i++) {
        let approval_subject = all_approval_subjects[i]
        let regular_subject = getSubjectFromTree(regular_tree, approval_subject.id)

        if(isEnrollable(approval_subject, regular_subject, approval_tree, regular_tree)){
            approval_subject.is_enrollable = true
            regular_subject.is_enrollable = true
        }
        else{
            regular_subject.is_enrollable = false
            approval_subject.is_enrollable = false
        }

        if (approval_subject.is_approved){
            if (approval_subject.all_approved) {
                if (isAllApproved(approval_subject, approval_tree, career)){
                    continue
                }
                else{
                    approval_subject.is_approved = false
                    regular_subject.is_regular = false
                }
            }
            if (isEnrollable(approval_subject, regular_subject, approval_tree, regular_tree) && isApprovable(approval_subject, regular_subject, approval_tree, regular_tree)) {
                continue
            }
            else{
                approval_subject.is_approved = false
                regular_subject.is_regular = false
            }
        }

        if (regular_subject.is_regular){
            if (isEnrollable(approval_subject, regular_subject, approval_tree, regular_tree)){
                continue
            }
            else {
                regular_subject.is_regular = false
            }
        }
    }
    changeHtmlStates(approval_tree, regular_tree)
}


function setAsApproved(approval_subject, regular_subject){
    approval_subject.is_approved = true
    regular_subject.is_regular = true
}


function setAsNull(approval_subject, regular_subject){
    approval_subject.is_approved = false
    regular_subject.is_regular = false
}


function setAsRegular(approval_subject, regular_subject){
    approval_subject.is_approved = false
    regular_subject.is_regular = true
}


function isAllApproved(approval_subject, approval_tree, career){
    const all_subjects = Object.values(approval_tree).flat()

    let only_subjects_before = []
    let only_subjects_after = []

    for (let i = 0; i < all_subjects.length; i++) {
        const subject = all_subjects[i]
        if (subject.id < approval_subject.id){
            only_subjects_before.push(subject)
        }
        else if (subject.id > approval_subject.id){
            // special case, sistemas has 2 'final projects'
            if (career !== 'sistemas'){
                only_subjects_after.push(subject)
            }
        }
        
    }

    for (let i = 0; i < only_subjects_after.length; i++) {
        const subject = only_subjects_after[i];
        if (!(subject.is_approved)){
            return false
        }
        
    }

    for (let i = 0; i < only_subjects_before.length; i++) {
        const subject = only_subjects_before[i];
        if (!(subject.is_approved)){
            return false
        }
        
    }
    return true
}


function changeState(element, approval_tree, regular_tree, career){
    // cambia el estado de is_approved e is_regular en ambos arboles y luego llama a updateTrees para aplicar los cambios
    let element_id = element.id.split('_')[1]
    
    let approval_subject = getSubjectFromTree(approval_tree, element_id)
    let regular_subject = getSubjectFromTree(regular_tree, element_id)
    let state = element.getAttribute('data-state')

    if(state === 'null'){
        // it's ingreso, it can't be regular
        if (element_id === '0'){
            if(!(approval_subject.is_enrollable && regular_subject.is_enrollable)){
                console.error(`${approval_subject.name} it's not enrollable yet`)
                return
            }
            
            if (approval_subject.all_approved){
                if (isAllApproved(approval_subject, approval_tree, career)){
                    setAsApproved(approval_subject, regular_subject)
                }
                else{
                    setAsRegular(approval_subject, regular_subject)
                }
            }
            
            else{
                setAsApproved(approval_subject, regular_subject)
            }

        }
        else{
            if(!(approval_subject.is_enrollable && regular_subject.is_enrollable)){
                console.error(`${approval_subject.name} it's not enrollable yet`)
                return
            }
        
            setAsRegular(approval_subject, regular_subject)
        }
    }
    else if(state === 'regular'){
        if (approval_subject.all_approved){
            if (isAllApproved(approval_subject, approval_tree, career)){
                setAsApproved(approval_subject, regular_subject)
            }
            else{
                setAsNull(approval_subject, regular_subject)
            }
        }
        
        else{
            setAsApproved(approval_subject, regular_subject)
        }
    }
    else if(state === 'approved'){
        setAsNull(approval_subject, regular_subject)
    }
    updateTrees(approval_tree, regular_tree, career)
}


function setEventListeners(classname1, classname2, approval_tree, regular_tree, career){
    // setea los event listeners de todos los divs (slots)
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
            changeState(element, approval_tree, regular_tree, career)
        })
    })
}


function generateTree(approval_tree, regular_tree, career) {
    // genera el grid de subjects y luego lo rellena con los subjects del arbol de aprobacion

    const container = document.getElementById('grid-container')
    const years = Object.values(approval_tree)
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
    changeSubjectStyle('subject', '#eaeaf7', 0, '')
    // sets onClick event listeners to all inUse elements
    setEventListeners('subject', 'inUse', approval_tree, regular_tree, career)

    // special case, it has 6 years instead of 5
    if (career === 'electronica'){
        let elements = Array.from(document.querySelectorAll('#grid-container > *:not(.inUse)'))
        console.log(elements)
        elements = elements.slice(21,24)
        for (let i = 0; i < elements.length; i++) {
            let element = elements[i]
            element.id = `subject_${37 + i}`
            element.setAttribute('data-state', 'null')
            element.className = element.className + ' inUse'
            element.style.backgroundColor = '#b5dcf7'
            element.style.border = '1px solid #577d97'
            element.textContent = approval_tree['year_6'][i].name
            element.addEventListener('click', function(e){
                changeState(element, approval_tree, regular_tree, career)
            })
        }
    }

}