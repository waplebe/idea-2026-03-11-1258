from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'tasks.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with app.app_context():
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
    conn.close()

init_db()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    if task is None:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify(dict(task))

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    task_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'id': task_id, 'title': title, 'description': description}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    conn = get_db_connection()
    conn.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?', (title, description, task_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task updated'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})

@app.route('/tasks', methods=['POST'])
def create_task_frontend():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    task_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'id': task_id, 'title': title, 'description': description}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_frontend(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})

@app.route('/tasks', methods=['GET'])
def get_tasks_with_pagination(page=1, limit=10):
    """
    Retrieves tasks with pagination support.

    Args:
        page (int, optional): The page number. Defaults to 1.
        limit (int, optional): The number of tasks per page. Defaults to 10.

    Returns:
        JSON: A JSON response containing the tasks for the specified page and limit.
    """
    offset = (page - 1) * limit
    conn = get_db_connection()
    tasks = conn.execute('''
        SELECT * FROM tasks
        LIMIT ? OFFSET ?
    ''', (limit, offset)).fetchall()
    conn.close()
    total_tasks = conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
    return jsonify({
        'tasks': [dict(task) for task in tasks],
        'total_pages': (total_tasks + limit - 1) // limit,
        'current_page': page,
        'limit': limit
    })

if __name__ == '__main__':
    app.run(debug=True)