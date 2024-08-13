from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error
from connect_db import get_db_connection

app = Flask(__name__)
ma = Marshmallow(app)


class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("name", "age")


class WorkoutSchema(ma.Schema):
    session_date = fields.Date(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ("session_date", "session_time", "activity")


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)


# Task 2 CRUD operations
@app.route("/members", methods=["POST"])
def add_member():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error:": "Could not connect to database"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "INSERT INTO members (name,age) VALUES (%s,%s)"
        new_customer = (customer_data["name"], customer_data["age"])
        cursor.execute(query, new_customer)
        conn.commit()
        return jsonify({"Message": "User added"}), 201
    except Error as e:
        print(e)
        return jsonify({"Error:": "Could not connect to database"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["GET"])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error:": "Could not connect to database"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM members WHERE id = %s"
        cursor.execute(query, (id,))
        user = cursor.fetchone()
        return customer_schema.jsonify(user)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error:": "Could not write to database"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error:": "Could not connect to database"}), 500
        cursor = conn.cursor(dictionary=True)
        customer_update = (customer_data["name"], customer_data["age"], id)
        query = "UPDATE members SET name = %s, age = %s WHERE id = %s"
        cursor.execute(query, customer_update)
        conn.commit()
        return jsonify({"Message": "User updated"}), 200
    except Error as e:
        pass
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error:": "Could not connect to database"}), 500
        cursor = conn.cursor()
        query = "DELETE FROM members WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        return jsonify({"Message": "User deleted"}), 200
    except Error as e:
        print(e)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/workoutsessions/<int:id>", methods=["GET"])
def get_workout_sessions(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error:": "Could not connect to database"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM workoutsessions WHERE member_id = %s"
        cursor.execute(query, (id,))
        sessions = cursor.fetchall()
        return workouts_schema.jsonify(sessions)
    except Error as e:
        print(e)
        return jsonify({"Error": "could not communicate with server"})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
