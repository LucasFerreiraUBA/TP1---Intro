function handle_response(data) {
    if (data.success) {
      alert("Se pudo crear el empleado");
      window.location.href = `/employees`;
    } else {
      alert(`error: ${data.message}`);
    }
  }

function create_employee(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const first_name = formData.get("first_name");
    const last_name = formData.get("last_name");
    const dni = formData.get("dni");
    const check_in_time = formData.get("check_in_time");
    const check_out_time = formData.get("check_out_time");

    fetch("http://localhost:5000/api/v1/employees", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        first_name: first_name,
        last_name: last_name,
        dni: dni,
        check_in_time: check_in_time,
        check_out_time: check_out_time,
        }),
    })
    .then((res) => res.json())
    .then(handle_response)
    .catch((error) => console.log("error:", error));
}