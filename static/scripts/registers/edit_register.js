const parameters = new URLSearchParams(window.location.search)
const id = parameters.get("id")

if (id == null) {
    window.location.href = "/"
}

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

function handle_get_register_response(data) {
    const option = document.getElementById(`${data.employee.id}`)
    option.setAttribute('selected', 'selected')
    document.getElementById("is_check_in_" + data.is_check_in).checked = true
    document.getElementById("timestamp").value = data.check_timestamp.split("T")[1]
    document.getElementById("date_edited").value = data.check_timestamp.split("T")[0]
}

fetch(`http://localhost:5000/api/v1/registers/${id}`, {method:"GET"})
.then((res) => res.json())
.then(handle_get_register_response)
.catch((error) => console.log("error:", error))

function handle_response(data) {
    if (data.success) {
        alert("Registro editado")
    }else {
        alert("Error al editar registro")
    }
}

function edit_register(event) {
    event.preventDefault()
    const formData = new FormData(event.target)
    const employee_id = formData.get("employees")
    const timestamp = formData.get("timestamp")
    const date_edited = formData.get("date_edited")
    const is_check_in = formData.get("is_check_in")
    const check_timestamp = `${date_edited}T${timestamp}`
    
    fetch(`http://localhost:5000/api/v1/registers/${id}`,
    {
        method:"PUT",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            employee_id: employee_id,
            check_timestamp: check_timestamp,
            is_check_in: is_check_in })
    })
    .then((res) => res.json())
    .then(handle_response)
    .catch((error) => console.log("error", error))
}