import unittest
from app import app, db

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/data_cs_test'  # Use a different database for testing
        self.app = app.test_client()

        # Create the test database and tables
        with app.app_context():
            cursor = db.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS data_cs_test')
            cursor.execute('USE data_cs_test')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            ''')
            db.commit()

    def tearDown(self):
        # Drop the test database after testing
        with app.app_context():
            cursor = db.cursor()
            cursor.execute('DROP DATABASE IF EXISTS data_cs_test')
            db.commit()

    def test_get_item(self):
        response = self.app.get('/api/item/1')
        self.assertEqual(response.status_code, 404)

        # Assuming you have added an item with ID 1 in the setup
        response = self.app.get('/api/item/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Laptop', response.data)

    def test_create_item(self):
        data = {
            "name": "New Test Item",
            "description": "Description for the new test item."
        }

        response = self.app.post('/api/item/1', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'Item created successfully')

    def test_update_item(self):
        data = {
            "name": "Updated Test Laptop",
            "description": "Updated description for the test laptop."
        }

        response = self.app.put('/api/item/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Item updated successfully')

    def test_delete_item(self):
        response = self.app.delete('/api/item/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Item deleted successfully')

if __name__ == '__main__':
    unittest.main()
