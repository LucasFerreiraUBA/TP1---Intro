function search_registers() {
    const num = document.getElementById("num_registers").value;
    document.getElementById("registers_list").innerHTML = "";
    fetch(`http://localhost:5000/api/v1/registers?limit=${num}`)
    .then((res) => res.json())
    .then(handle_data)
    .catch((error) => console.log("error:", error));
}

function handle_delete_request(data) {
    if (data.success) {
        alert("Registro Borrado Exitosamente!");
    } else {
        alert("Error. No se pudo eliminar");
    }
}

function delete_register(id) {
    const confirm_popup = confirm("¿Estás seguro de eliminar el registro?");
    if (confirm_popup) {
        fetch(`http://localhost:5000/api/v1/registers/${id}`, {
        method: "DELETE",
        })
        .then((res) => res.json())
        .then(handle_delete_request)
        .catch((error) => console.log("error:", error));
        document.getElementById(id).remove();
    }
}

function edit_register(id) {
    window.location.href = `registers/edit?id=${id}`;
}

function print_is_input(is_check_in) {
    if (is_check_in) {
        return "Entrada";
    }
    return "Salida";
}

function handle_data(data) {
    const container = document.getElementById("registers_list");
    for (const register of data) {
        const employee = register.employee;
        const card = document.createElement("div");
        const register_name = document.createElement("h6");
        const register_date = document.createElement("input");
        const register_time = document.createElement("input");
        const register_is_check_in = document.createElement("p");
        const edit_button = document.createElement("button");
        const delete_button = document.createElement("button");

        card.setAttribute("id", `${register.id}`);
        card.setAttribute("class", "register-card");

        register_date.setAttribute("type", "date");
        register_date.setAttribute("disabled", "disabled");

        register_time.setAttribute("type", "time");
        register_time.setAttribute("disabled", "disabled");

        edit_button.setAttribute("onclick", `edit_register(${register.id})`);
        delete_button.setAttribute(
        "onclick",
        `delete_register(${register.id})`
        );

        register_name.innerText = `${employee.last_name}, ${employee.first_name}`;
        register_date.value = register.timestamp.split("T")[0];
        register_time.value = register.timestamp.split("T")[1].slice(0, 5);
        register_is_check_in.innerText = print_is_input(register.is_check_in);

        let pill_class;
        register.is_check_in
        ? (pill_class = "check_in")
        : (pill_class = "check_out");
        register_is_check_in.setAttribute("class", `${pill_class}`);

        let deviation = Math.trunc(register.deviation_seconds / 60);
        const deviation_mark = document.createElement("p");
        deviation_mark.innerText = `${deviation} min`;

        edit_button.innerText = "Editar";
        delete_button.innerText = "Borrar";

        card.append(register_name);
        card.append(register_date);
        card.append(register_time);
        card.append(register_is_check_in);
        card.append(edit_button);
        card.append(delete_button);
        card.append(deviation_mark);
        container.append(card);
    }
}

fetch("http://localhost:5000/api/v1/registers")
.then((res) => res.json())
.then(handle_data)
.catch((error) => console.log("error:", error));