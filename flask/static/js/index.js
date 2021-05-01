function updateFormAction(e) {
    id = e.dataset['id'];
    endpoint = e.dataset['endpoint'];
    form = document.getElementById(`form-${id}`);
    form.action = `/${endpoint}/${e.value}`
}
