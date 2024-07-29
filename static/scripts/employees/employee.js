const url = window.location.pathname.split("/");
const id = url[url.length - 1];

function replace_predet(input, predet) {
    var input_value = input.value;
    return input_value === "" ? predet : input_value;
}

function search_unpunctuals() {
    document.getElementById("unpunctual_list").innerHTML = "";
    const input_in = document.getElementById("entering_tolerancy");
    const input_out = document.getElementById("leaving_tolerancy");

    const v1 = replace_predet(input_in, 0);
    const v2 = replace_predet(input_out, 0);

    fetch(
        `http://localhost:5000/api/v1/employees/${id}/registers/unpunctual?entering_tolerancy=${v1}&leaving_tolerancy=${v2}`
    )
    .then((res) => res.json())
    .then(handle_unpunctual_data)
    .catch((error) => console.log("error:", error));
}

function handle_get_response(data) {
    document.getElementById("employee_name").innerText = `${data.last_name}, ${data.first_name}`;
    document.getElementById("name").innerText = `Nombre: ${data.last_name}, ${data.first_name}`;
    document.getElementById("dni").innerText = `DNI: ${data.dni}`;
    document.getElementById("check_in_time").value =data.check_in_time.slice(0, 5);
    document.getElementById("check_out_time").value =data.check_out_time.slice(0, 5);
}

fetch(`http://localhost:5000/api/v1/employees/${id}`, { method: "GET" })
.then((res) => res.json())
.then(handle_get_response)
.catch((error) => console.log("error:", error));

function print_is_input(is_check_in) {
    if (is_check_in) {
        return "Entrada";
    }
    return "Salida";
}

function handle_data(data) {
    const container = document.getElementById("registers_list");
    for (const register of data) {
        const card = document.createElement("li");
        const register_date = document.createElement("input");
        const register_time = document.createElement("input");
        const register_is_check_in = document.createElement("p");

        card.setAttribute("id", `${register.id}`);
        card.setAttribute("class", "register-card")
        register_date.setAttribute("type", "date");
        register_date.setAttribute("disabled", "disabled");
        register_time.setAttribute("type", "time");
        register_time.setAttribute("disabled", "disabled");
        register_date.value = register.check_timestamp.split("T")[0];
        register_time.value = register.check_timestamp
        .split("T")[1]
        .slice(0, 5);
        register_is_check_in.innerText = print_is_input(register.is_check_in);

        let pill_class;
        register.is_check_in
        ? (pill_class = "check_in")
        : (pill_class = "check_out");
        register_is_check_in.setAttribute("class", `${pill_class}`);
        
        let deviation = Math.trunc(register.deviation_seconds / 60);
        const deviation_mark = document.createElement("p");
        deviation_mark.innerText = `${deviation} min`;

        card.append(register_date);
        card.append(register_time);
        card.append(register_is_check_in);
        card.append(deviation_mark)
        container.append(card);
    }
}

function handle_unpunctual_data(data) {
    const container = document.getElementById("unpunctual_list");
    for (const register of data) {
        const card = document.createElement("li");
        const register_date = document.createElement("input");
        const register_time = document.createElement("input");
        const register_is_check_in = document.createElement("p");

        card.setAttribute("id", `${register.id}`);
        card.setAttribute("class", "register-card")
        register_date.setAttribute("type", "date");
        register_date.setAttribute("disabled", "disabled");
        register_time.setAttribute("type", "time");
        register_time.setAttribute("disabled", "disabled");
        register_date.value = register.check_timestamp.split("T")[0];
        register_time.value = register.check_timestamp
        .split("T")[1]
        .slice(0, 5);
        register_is_check_in.innerText = print_is_input(register.is_check_in);

        let pill_class;
        register.is_check_in
        ? (pill_class = "check_in")
        : (pill_class = "check_out");
        register_is_check_in.setAttribute("class", `${pill_class}`);

        let deviation = Math.trunc(register.deviation_seconds / 60);
        const deviation_mark = document.createElement("p");
        deviation_mark.innerText = `${deviation} min`;

        card.append(register_date);
        card.append(register_time);
        card.append(register_is_check_in);
        card.append(deviation_mark);
        container.append(card);
    }
}

fetch(`http://localhost:5000/api/v1/employees/${id}/registers/`)
.then((res) => res.json())
.then(handle_data)
.catch((error) => console.log("error:", error));

fetch(`http://localhost:5000/api/v1/employees/${id}/registers/unpunctual/`)
.then((res) => res.json())
.then(handle_unpunctual_data)
.catch((error) => console.log("error:", error));