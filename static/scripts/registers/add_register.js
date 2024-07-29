function handle_get_employees_response(data) {
    const employees = document.getElementById("employees")
    for (const item of data) {
        const option = document.createElement("option")
        option.innerText = item.last_name + ", " + item.first_name
        option.setAttribute("value", `${item.id}`)
        option.setAttribute("id", `${item.id}`)
        employees.append(option);
    }
}

fetch(`http://localhost:5000/api/v1/employees`, {method:"GET"})
.then((res) => res.json())
.then(handle_get_employees_response)
.catch((error) => console.log("error", error))

function handle_response(data) {
    if (data.success) {
        alert("Registro agregado")
    }else {
        alert("Error al agregar el registro")
    }
}

function create_register(event) {
    event.preventDefault()
    const formData = new FormData(event.target)
    const employee_id = formData.get("employees")
    const timestamp = formData.get("timestamp")
    const date_edited = formData.get("date_edited")
    const check_timestamp = `${date_edited}T${timestamp}`
    
    fetch(`http://localhost:5000/api/v1/registers`,
    {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            employee_id: employee_id,
            timestamp: check_timestamp })
    })
    .then((res) => res.json())
    .then(handle_response)
    .catch((error) => console.log("error", error))
}