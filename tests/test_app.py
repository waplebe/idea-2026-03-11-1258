import unittest
from unittest.mock import patch
from app import app

class TestTasks(unittest.TestCase):

    @patch('app.get_db_connection')
    def test_get_tasks(self, mock_db_connection):
        mock_db_connection.return_value.execute.return_value.fetchall.return_value = [
            {'id': 1, 'title': 'Task 1', 'description': 'Description 1'},
            {'id': 2, 'title': 'Task 2', 'description': 'Description 2'}
        ]
        response = app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['tasks'], [{'id': 1, 'title': 'Task 1', 'description': 'Description 1'}, {'id': 2, 'title': 'Task 2', 'description': 'Description 2'}])

    @patch('app.get_db_connection')
    def test_get_task(self, mock_db_connection):
        mock_db_connection.return_value.execute.return_value.fetchone.return_value = {'id': 1, 'title': 'Task 1', 'description': 'Description 1'}
        response = app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 1, 'title': 'Task 1', 'description': 'Description 1'})

    @patch('app.get_db_connection')
    def test_create_task(self, mock_db_connection):
        mock_db_connection.return_value.execute.return_value.last_insert_rowid.return_value = 1
        mock_db_connection.return_value.commit.return_value = None
        data = {'title': 'New Task', 'description': 'New Description'}
        response = app.post('/tasks', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['title'], 'New Task')
        self.assertEqual(response.json['description'], 'New Description')

    @patch('app.get_db_connection')
    def test_update_task(self, mock_db_connection):
        mock_db_connection.return_value.execute.return_value.last_insert_rowid.return_value = 1
        mock_db_connection.return_value.commit.return_value = None
        data = {'title': 'Updated Task', 'description': 'Updated Description'}
        response = app.put('/tasks/1', json=data)
        self.assertEqual(response.status_code, 200)

    @patch('app.get_db_connection')
    def test_delete_task(self, mock_db_connection):
        mock_db_connection.return_value.execute.return_value.last_insert_rowid.return_value = 1
        mock_db_connection.return_value.commit.return_value = None
        response = app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)

    @patch('app.get_db_connection')
    def test_get_tasks_with_pagination(self, mock_db_connection):
        mock_db_connection.return_value.execute.return_value.fetchall.return_value = [
            {'id': 1, 'title': 'Task 1', 'description': 'Description 1'},
            {'id': 2, 'title': 'Task 2', 'description': 'Description 2'},
            {'id': 3, 'title': 'Task 3', 'description': 'Description 3'}
        ]
        response = app.get('/tasks?page=2&limit=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['tasks']), 2)
        self.assertEqual(response.json['current_page'], 2)
        self.assertEqual(response.json['limit'], 2)
        self.assertEqual(response.json['total_pages'], 2)

if __name__ == '__main__':
    unittest.main()