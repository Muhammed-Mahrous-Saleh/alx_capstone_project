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

    var titleLabel = document.createElement('label');
    titleLabel.innerText = 'Title:';
    titleLabel.htmlFor = 'subtask_title_' + subtaskCount;
    newSubtaskDiv.appendChild(titleLabel);

    var titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.name = 'subtask_title_' + subtaskCount;
    titleInput.required = true;
    newSubtaskDiv.appendChild(titleInput);
    newSubtaskDiv.appendChild(document.createElement('br'));

    var statusLabel = document.createElement('label');
    statusLabel.innerText = 'Status:';
    statusLabel.htmlFor = 'subtask_status_' + subtaskCount;
    newSubtaskDiv.appendChild(statusLabel);

    var statusInput = document.createElement('select');
    statusInput.name = 'subtask_status_' + subtaskCount;
    ['Not Started', 'In Progress', 'Completed'].forEach(function (statusOption) {
        var option = document.createElement('option');
        option.value = statusOption;
        option.innerText = statusOption;
        statusInput.appendChild(option);
    });
    newSubtaskDiv.appendChild(statusInput);
    newSubtaskDiv.appendChild(document.createElement('br'));

    var dueDateLabel = document.createElement('label');
    dueDateLabel.innerText = 'Due Date:';
    dueDateLabel.htmlFor = 'subtask_due_date_' + subtaskCount;
    newSubtaskDiv.appendChild(dueDateLabel);

    var dueDateInput = document.createElement('input');
    dueDateInput.type = 'date';
    dueDateInput.name = 'subtask_due_date_' + subtaskCount;
    newSubtaskDiv.appendChild(dueDateInput);
    newSubtaskDiv.appendChild(document.createElement('br'));

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
        deleteButton.parentElement.remove();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    console.log(new Date().getDate())
    
    console.log(document.getElementById('start_date').value)
});