function handle_get_response(data) {
    const employees = document.getElementById("employees")
    for (const item of data) {
        const opcion = document.createElement("option")
        opcion.innerText = item.last_name + ", " + item.first_name
        opcion.setAttribute("value", `${item.id}`)
        employees.append(opcion);
    }
}

fetch(`http://localhost:5000/api/v1/employees`, {method:"GET"})
.then((res) => res.json())
.then(handle_get_response)
.catch((error) => console.log("error", error))

function handle_response(data) {
    if (data.success) {
        alert("Registro agregado")
    }else {
        alert("Error al crear registro")
    }
}

function create_register(event) {
    event.preventDefault()
    const formData = new FormData(event.target)
    const employee_id = formData.get("employees")
    const timestamp = formData.get("timestamp")
    const date = new Date()
    const date_str = date.toISOString().split('T')[0]
    const check_timestamp = `${date_str}T${timestamp}`

    fetch(`http://localhost:5000/api/v1/registers`,
    {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            employee_id: employee_id,
            timestamp: check_timestamp,
        })
    })
    .then((res) => res.json())
    .then(handle_response)
    .catch((error) => console.log("ERROR", error))
}