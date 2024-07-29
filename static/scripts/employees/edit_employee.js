const parameters = new URLSearchParams(window.location.search)
const id = parameters.get("id")

if (id == null) {
    window.location.href = "/"
}

function handle_get_response(data) {
    document.getElementById("first_name").value = data.first_name
    document.getElementById("last_name").value = data.last_name
    document.getElementById("dni").value = data.dni
    document.getElementById("check_in_time").value = data.check_in_time
    document.getElementById("check_out_time").value = data.check_out_time
}

fetch(`http://localhost:5000/api/v1/employees/${id}`, {method:"GET"})
.then((res) => res.json())
.then(handle_get_response)
.catch((error) => console.log("error:", error))

function handle_response(data) {
    if (data.success) {
        alert("Empleado Modificado")
        window.location.href = `/employees`
    } else {
        alert("Error al editar al empleado")
    }
}

function edit_employee(event) {
    event.preventDefault()
    const formData = new FormData(event.target)
    const first_name = formData.get("first_name")
    const last_name = formData.get("last_name")
    const dni = formData.get("dni")
    const check_in_time = formData.get("check_in_time")
    const check_out_time = formData.get("check_out_time")

    fetch(`http://localhost:5000/api/v1/employees/${id}`, 
    {
        method:"PUT",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            first_name: first_name,
            last_name: last_name,
            dni: dni,
            check_in_time: check_in_time,
            check_out_time: check_out_time
        })
    })
    .then((res) => res.json())
    .then(handle_response)
    .catch((error) => console.log("ERROR", error))
}