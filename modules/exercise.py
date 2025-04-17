# modules/exercise.py
from flask import Blueprint, request, jsonify, current_app
import pymysql

bp = Blueprint('exercise', __name__)

def get_db_connection():
    config = current_app.config
    return pymysql.connect(
        host=config['MYSQL_HOST'],
        user=config['MYSQL_USER'],
        password=config['MYSQL_PASSWORD'],
        db=config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@bp.route('/record', methods=['POST'])
def record_exercise():
    data = request.get_json()
    steps = data.get('steps')
    stride = data.get('stride_length')
    weight = data.get('weight')
    intensity = data.get('intensity')
    types = ','.join(data.get('exercise_types', []))
    date = data.get('date')

    if not all([steps, stride, weight, date]):
        return jsonify({'error': '缺少必要字段'}), 400

    sql = "INSERT INTO exercise (date, steps, stride_length, weight, intensity, exercise_types) VALUES (%s, %s, %s, %s, %s, %s)"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (date, steps, stride, weight, intensity, types))
        conn.commit()
        return jsonify({'message': '运动数据保存成功'})
    finally:
        conn.close()
