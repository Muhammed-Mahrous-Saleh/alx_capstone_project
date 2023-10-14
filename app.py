from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import date
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.before_first_request
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Task (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            DueDate TEXT,
            Status TEXT NOT NULL,
            Category TEXT,
            Priority INTEGER,
            Reminder TEXT,
            StartDate TEXT
        )
        ''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS SubTask (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Status TEXT NOT NULL,
            DueDate TEXT,
            TaskID INTEGER,
            FOREIGN KEY(TaskID) REFERENCES Task(ID)
        )
        ''')


@app.route('/')
def main_screen():
    sort_option = request.args.get('sort', 'DueDate')
    filter_option = request.args.get('filter', 'all')
    search_term = request.args.get('search', '')

    conn = get_db_connection()

    # Base query with subtask count logic
    query = '''
        SELECT 
            Task.*,
            COUNT(SubTask.ID) AS total_subtasks,
            SUM(CASE WHEN SubTask.status = 'Completed' THEN 1 ELSE 0 END) AS completed_subtasks
        FROM Task
        LEFT JOIN SubTask ON Task.ID = SubTask.TaskID
    '''
    params = []

    # Add conditions for search and filter
    conditions = []
    if search_term != '':
        conditions.append(
            'Task.Title LIKE ? OR Task.Description LIKE ? OR Task.Category LIKE ?')
        params.extend(['%' + search_term + '%'] * 3)
    if filter_option != 'all':
        conditions.append('Task.Status = ?')
        params.append(filter_option)

    # Add conditions to query
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    # Add group by and sorting to query
    query += ' GROUP BY Task.ID'
    query += ' ORDER BY ' + sort_option
    if sort_option == 'Title':
        query += ' COLLATE NOCASE'

    tasks = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('main.html', tasks=tasks, search_term=search_term)


@app.route('/task/<int:task_id>')
def task_screen(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM Task WHERE ID = ?',
                        (task_id,)).fetchone()

    today = date.today()
    # Fetch subtasks if task exists
    subtasks = []
    if task:
        subtasks = conn.execute(
            'SELECT * FROM SubTask WHERE TaskID = ?', (task_id,)).fetchall()

    conn.close()
    return render_template('task.html', task=task, subtasks=subtasks, today=today)


@app.route('/save_task/<int:task_id>', methods=['POST'])
def save_task(task_id):
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = request.form.get('due_date')
    status = request.form.get('status')
    category = request.form.get('category')
    priority = request.form.get('priority')
    reminder = request.form.get('reminder')
    start_date = request.form.get('start_date')

    with get_db_connection() as conn:
        # If task_id is 0, it's a new task. Otherwise, update the existing task.
        if task_id == 0:
            cur = conn.execute('''
                INSERT INTO Task (Title, Description, DueDate, Status, Category, Priority, Reminder, StartDate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, due_date, status, category, priority, reminder, start_date))
            # Get the new task id
            task_id = cur.lastrowid
        else:
            conn.execute('''
                UPDATE Task 
                SET Title = ?, Description = ?, DueDate = ?, Status = ?, Category = ?, Priority = ?, Reminder = ?, StartDate = ?
                WHERE ID = ?
            ''', (title, description, due_date, status, category, priority, reminder, start_date, task_id))

        # Process and save subtasks
        i = 1
        while True:
            # Get subtask data
            subtask_id = request.form.get('subtask_id_' + str(i))
            subtask_title = request.form.get('subtask_title_' + str(i))
            subtask_status = request.form.get('subtask_status_' + str(i))
            subtask_due_date = request.form.get('subtask_due_date_' + str(i))

            # Break the loop if no more subtask data is found
            if subtask_title is None:
                break

            if int(subtask_id) == 0:  # New subtask
                # Save subtask to database
                conn.execute('''
                    INSERT INTO SubTask (Title, Status, DueDate, TaskID)
                    VALUES (?, ?, ?, ?)
                ''', (subtask_title, subtask_status, subtask_due_date, task_id))
            else:  # Existing subtask
                # Update subtask in the database
                conn.execute('''
                    UPDATE SubTask
                    SET Title = ?, Status = ?, DueDate = ?
                    WHERE ID = ? AND TaskID = ?
                ''', (subtask_title, subtask_status, subtask_due_date, subtask_id, task_id))

            i += 1

    return redirect(url_for('main_screen'))


@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM Task WHERE ID = ?', (task_id,))
    return redirect(url_for('main_screen'))


@app.route('/delete_subtask/<int:subtask_id>', methods=['POST'])
def delete_subtask(subtask_id):
    with get_db_connection() as conn:
        # Get the main task id for redirecting later
        task_id = conn.execute(
            'SELECT TaskID FROM SubTask WHERE ID = ?', (subtask_id,)).fetchone()[0]
        # Delete the subtask
        conn.execute('DELETE FROM SubTask WHERE ID = ?', (subtask_id,))
    return redirect(url_for('task_screen', task_id=task_id))


@app.route('/check_reminders')
def check_reminders():
    with get_db_connection() as conn:
        reminders = conn.execute(
            'SELECT * FROM Task WHERE Reminder <= datetime("now", "+5 minutes") AND Reminder >= datetime("now")').fetchall()
    return jsonify([dict(r) for r in reminders])


@app.route('/abort_changes/<int:task_id>', methods=['POST'])
def abort_changes(task_id):

    # Retrieve original subtasks.
    original_subtasks = request.get_json().get('subtasks', [])
    print("Received data:", original_subtasks)
    with get_db_connection() as conn:
        print("got in point 1")
        # Delete current subtasks in SubTask.
        conn.execute('DELETE FROM SubTask WHERE TaskID = ?', (task_id,))
        print("got in point 2")
        # Insert original subtasks back into SubTask.
        for subtask in original_subtasks:
            conn.execute('''
                INSERT INTO SubTask (ID, Title, Status, DueDate, TaskID)
                VALUES (?, ?, ?, ?, ?)
            ''', (subtask['ID'], subtask['Title'], subtask['Status'], subtask['DueDate'], task_id))
    print("got in point 3")
    return redirect(url_for('task_screen', task_id=task_id))


if __name__ == '__main__':
    app.run(debug=False)
