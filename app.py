# app.py
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import mysql.connector

app = Flask(__name__)
api = Api(app)

# MySQL Configuration
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="data_cs"
)

cursor = db.cursor()

class ItemResource(Resource):
    def get(self, item_id):
        # Read operation
        query = "SELECT * FROM items WHERE id = %s"
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()

        if result:
            item_dict = {
                "id": result[0],
                "name": result[1],
                "description": result[2]
            }
            return jsonify(item_dict)

        return {"message": "Item not found"}, 404

    def post(self, item_id):
        # Create operation
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")

        query = "INSERT INTO items (name, description) VALUES (%s, %s)"
        cursor.execute(query, (name, description))
        db.commit()

        return {"message": "Item created successfully"}, 201

    def put(self, item_id):
        # Update operation
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")

        query = "UPDATE items SET name = %s, description = %s WHERE id = %s"
        cursor.execute(query, (name, description, item_id))
        db.commit()

        return {"message": "Item updated successfully"}

    def delete(self, item_id):
        # Delete operation
        query = "DELETE FROM items WHERE id = %s"
        cursor.execute(query, (item_id,))
        db.commit()

        return {"message": "Item deleted successfully"}

api.add_resource(ItemResource, '/api/item/<int:item_id>')


if __name__ == '__main__':
    app.run(debug=True)
