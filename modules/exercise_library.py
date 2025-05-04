from flask import Blueprint, request, jsonify
import mysql.connector
from config import Config

bp = Blueprint('exercise_library', __name__)

@bp.route('/list', methods=['GET'])
def list_exercises():
    # 获取运动库列表
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM exercise_library')
    exercises = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(exercises)

@bp.route('/add', methods=['POST'])
def add_exercise():
    # 添加新运动到库
    data = request.json
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO exercise_library (name, description, muscle_group, equipment, difficulty, instructions) '
        'VALUES (%s, %s, %s, %s, %s, %s)',
        (data['name'], data['description'], data['muscle_group'], 
         data['equipment'], data['difficulty'], data['instructions'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Exercise added successfully'})
