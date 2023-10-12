document.getElementById('add_subtask').addEventListener('click', function () {
    var subtasksDiv = document.getElementById('subtasks');
    var subtaskCount = subtasksDiv.getElementsByClassName('subtask').length + 1;

    var newSubtaskDiv = document.createElement('div');
    newSubtaskDiv.className = 'subtask';

    var subtaskIdInput = document.createElement('input');
    subtaskIdInput.type = 'hidden';
    subtaskIdInput.name = 'subtask_id_' + subtaskCount;
    subtaskIdInput.value = '0';
    newSubtaskDiv.appendChild(subtaskIdInput);

    var titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.name = 'subtask_title_' + subtaskCount;
    titleInput.required = true;
    newSubtaskDiv.appendChild(titleInput);

    var statusInput = document.createElement('select');
    statusInput.name = 'subtask_status_' + subtaskCount;
    ['Not Started', 'In Progress', 'Completed'].forEach(function (statusOption) {
        var option = document.createElement('option');
        option.value = statusOption;
        option.innerText = statusOption;
        statusInput.appendChild(option);
    });
    newSubtaskDiv.appendChild(statusInput);

    var dueDateInput = document.createElement('input');
    dueDateInput.type = 'date';
    dueDateInput.name = 'subtask_due_date_' + subtaskCount;
    newSubtaskDiv.appendChild(dueDateInput);

    var deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.innerText = 'Delete Subtask';
    deleteButton.className = 'delete_subtask';
    deleteButton.addEventListener('click', function () {
        newSubtaskDiv.remove();
    });
    newSubtaskDiv.appendChild(deleteButton);
    newSubtaskDiv.appendChild(document.createElement('br'));
    newSubtaskDiv.appendChild(document.createElement('br'));

    subtasksDiv.appendChild(newSubtaskDiv);
});

document.querySelectorAll('.delete_subtask').forEach(function (deleteButton) {
    deleteButton.addEventListener('click', function () {
        let confirm_delete = confirm('Are you sure you want to delete this subtask?');
        if (confirm_delete) {
            // Get the subtask ID from a data attribute.
            const subtaskId = deleteButton.getAttribute('data-subtask-id');

            // Send a DELETE request to the server.
            fetch(`/delete_subtask/${subtaskId}`, {
                method: 'POST',
            })
                .then(response => {
                    if (response.ok) {
                        // If the request was successful, remove the subtask from the DOM.
                        deleteButton.closest('.subtask').remove();
                    } else {
                        console.error('Failed to delete subtask', response);
                    }
                })
                .catch(error => console.error('Error during fetch operation', error));
            deleteButton.parentElement.remove()
        }
    });
});
