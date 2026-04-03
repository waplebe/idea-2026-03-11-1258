document.addEventListener('DOMContentLoaded', function() {
    const newTaskButton = document.getElementById('newTaskButton');
    const taskList = document.getElementById('taskList');

    // Fetch tasks from the API
    fetch('/tasks')
        .then(response => response.json())
        .then(tasks => {
            taskList.innerHTML = ''; // Clear existing tasks
            tasks.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.innerHTML = `
                    <h3>${task.title}</h3>
                    <p>${task.description}</p>
                    <button class="deleteTaskButton" data-id="${task.id}">Delete</button>
                `;
                taskList.appendChild(taskElement);
            });
        })
        .catch(error => console.error('Error fetching tasks:', error));

    // Add new task
    newTaskButton.addEventListener('click', function() {
        // Implement adding new task functionality here
        // This is a placeholder
        alert('Add new task functionality not implemented.');
    });

    // Delete task
    taskList.addEventListener('click', function(event) {
        if (event.target.classList.contains('deleteTaskButton')) {
            const taskId = event.target.dataset.id;
            if (confirm('Are you sure you want to delete this task?')) {
                fetch(`/tasks/${taskId}`, { method: 'DELETE' })
                    .then(response => response.json())
                    .then(data => {
                        // Refresh task list after deletion
                        fetch('/tasks')
                            .then(response => response.json())
                            .then(tasks => {
                                taskList.innerHTML = '';
                                tasks.forEach(task => {
                                    const taskElement = document.createElement('div');
                                    taskElement.innerHTML = `
                                        <h3>${task.title}</h3>
                                        <p>${task.description}</p>
                                        <button class="deleteTaskButton" data-id="${task.id}">Delete</button>
                                    `;
                                    taskList.appendChild(taskElement);
                                });
                            });
                    });
            }
        }
    });
});