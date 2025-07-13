document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('edit-btn');
    const saveBtn = document.getElementById('save-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const inputs = document.querySelectorAll('#edit-form input');

    let originalValues = {};

    editBtn.addEventListener('click', () => {
        inputs.forEach(input => {
            originalValues[input.name] = input.value;
            input.removeAttribute('readonly');
        });
        editBtn.style.display = 'none';
        saveBtn.style.display = 'inline-block';
        cancelBtn.style.display = 'inline-block';
    });

    cancelBtn.addEventListener('click', () => {
        inputs.forEach(input => {
            input.value = originalValues[input.name];
            input.setAttribute('readonly', true);
        });
        editBtn.style.display = 'inline-block';
        saveBtn.style.display = 'none';
        cancelBtn.style.display = 'none';
    });
});