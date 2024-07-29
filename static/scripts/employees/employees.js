function search_employees() {
    const num = document.getElementById("num_employeers").value
    document.getElementById("employees_list").innerHTML = ""
    fetch(`http://localhost:5000/api/v1/employees?limit=${num}`)
    .then((res) => res.json())
    .then(handle_data)
    .catch((error) => console.log("error:", error))
}

function handle_delete_request(data) {
    if (data.success) {
        alert("Empleado Borrado Exitosamente!")
    } else {
        alert("Error. No se pudo eliminar")
    }
}

function delete_employee(id) {
    const confirm_popup = confirm("¿Estás seguro de eliminar al empleado?")
    if (confirm_popup) {
        fetch(`http://localhost:5000/api/v1/employees/${id}`, {method:"DELETE"})
        .then((res) => res.json())
        .then(handle_delete_request)
        .catch((error) => console.log("error:", error))
        document.getElementById(id).remove()
    } 
}

function edit_employee(id) {
    window.location.href = `employees/edit?id=${id}`
}

function get_employee(id) {
    window.location.href = `employees/${id}`
}

function handle_data(data) {
    const container = document.getElementById("employees_list")
    for (const employee of data) {

        const row = document.createElement("div")
        const employee_name = document.createElement("p")
        const delete_button = document.createElement("button")
        const edit_button = document.createElement("button")
        const more_button = document.createElement("button")

        row.setAttribute("id", `${employee.id}`)
        row.setAttribute("class","employee-card")
        delete_button.setAttribute("onclick", `delete_employee(${employee.id})`) 
        edit_button.setAttribute("onclick", `edit_employee(${employee.id})`)
        more_button.setAttribute("onclick", `get_employee(${employee.id})`)

        delete_button.setAttribute("class", "basic-button") 
        edit_button.setAttribute("class", "basic-button") 
        more_button.setAttribute("class", "basic-button")

        employee_name.innerText = `${employee.last_name}, ${employee.first_name}`
        edit_button.innerText = "Editar"
        delete_button.innerText = "Borrar"
        more_button.innerText = "Ver mas"
        
        row.append(employee_name)
        row.append(more_button)
        row.append(edit_button)
        row.append(delete_button)
        container.append(row)
    }
}

fetch("http://localhost:5000/api/v1/employees")
.then((res) => res.json())
.then(handle_data)
.catch((error) => console.log("error:", error))