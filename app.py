from flask import Flask
import sqlite3
from flask import Flask, request, jsonify

# from flask_cors import CORS

app = Flask(__name__)


# CORS(app, resources={r"/*": {"origins": "*"}})


def connect_to_db():
    '''
    Подключение к базе данных
    :return:
    '''
    conn = sqlite3.connect('tasks_db')
    return conn


def insert_task(task):
    '''
    Добавление задачи
    :param task: json object
    :return: dict
    '''
    inserted_task = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (name, desc, date_add, date_do, category_id, user_id)"
                    " VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        task['name'],
                        task['desc'],
                        task['date_add'],
                        task['date_do'],
                        task['category_id'],
                        task['user_id']
                    )
                    )
        conn.commit()
        inserted_task = get_task_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()


def get_task_by_id(task_id):
    '''

    :param task_id:
    :return: dict
    '''
    task = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        task["id"] = row["id"]
        task["name"] = row["name"]
        task["desc"] = row["desc"]
        task["date_add"] = row["date_add"]
        task["date_do"] = row["date_do"]
        task["category_id"] = row["category_id"]
        task["user_id"] = row["user_id"]
    except:
        task = {}

    return task


def get_tasks(user_id):
    '''

    :param user_id:
    :return: list
    '''
    tasks = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE user_id = ?",
                    (user_id,))
        rows = cur.fetchall()

        # convert row objects to dictionary
        for row in rows:
            task = {}
            task["id"] = row["id"]
            task["name"] = row["name"]
            task["desc"] = row["desc"]
            task["date_add"] = row["date_add"]
            task["date_do"] = row["date_do"]
            task["category_id"] = row["category_id"]
            task["user_id"] = row["user_id"]
            tasks.append(task)

    except:
        tasks = []

    return tasks


def update_task(task):
    '''
    Update row
    :param task: json object
    :return: dict row
    '''
    updated_task = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(" UPDATE tasks SET "
                    " name = ?, "
                    " desc = ?, "
                    " date_add = ?, "
                    " date_do = ?, "
                    " category_id = ?, "
                    " user_id = ? "
                    " WHERE id =? ",
                    (task["name"], task["desc"], task["date_add"],
                     task["date_do"], task["category_id"],
                     task["user_id"], task["id"]))
        conn.commit()

        updated_user = get_task_by_id(task["id"])

    except:
        conn.rollback()
        updated_task = {}
    finally:
        conn.close()

    return updated_task


def delete_task(task_id):
    '''

    :param task_id:
    :return:
    '''
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from tasks WHERE id = ?",
                     (task_id,))
        conn.commit()
        message["status"] = "Task deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete task"
    finally:
        conn.close()

    return message


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/tasks/<task_id>', methods=['GET'])
def api_get_task(task_id):
    return jsonify(get_task_by_id(task_id))


@app.route('/api/add_task', methods=['POST'])
def api_add_task():
    task = request.get_json()
    return jsonify(insert_task(task))


@app.route('/api/task-by-user/<user_id>', methods=['GET'])
def api_get_user_tasks(user_id):
    return jsonify(get_tasks(user_id))


@app.route('/api/task-update', methods=['PUT'])
def api_update_task():
    task = request.get_json()
    return jsonify(update_task(task))


@app.route('/api/task-delete/<task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    return jsonify(delete_task(task_id))


if __name__ == '__main__':
    app.run()
