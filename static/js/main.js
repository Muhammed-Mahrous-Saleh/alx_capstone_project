function checkReminders() {
    fetch('/check_reminders')
        .then(response => response.json())
        .then(reminders => {
            reminders.forEach(reminder => {
                var notification = new Notification('Reminder:', {
                    body: reminder.Title,
                });
                // Additional logic to handle notification click, etc.
            });
        })
        .catch(error => console.error('Error:', error));
}

// Check for reminders every minute
setInterval(checkReminders, 60000);

document.addEventListener('DOMContentLoaded', function () {
    // Check for notification availability.
    if (!Notification) {
        alert('Desktop notifications not available in your browser.');
        return;
    }
    if (Notification.permission !== 'granted') {
        Notification.requestPermission();
    }
});

document.getElementById("yearSpan").innerText = new Date().getFullYear();
