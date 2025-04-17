# modules/period.py
from flask import Blueprint, request, jsonify, current_app
import pymysql

bp = Blueprint('period', __name__)

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
def record_period():
    data = request.get_json()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    flow = data.get('flow')
    symptoms = ','.join(data.get('symptoms', []))
    mood = data.get('mood')
    notes = data.get('notes')

    if not start_date or not flow:
        return jsonify({'error': '缺少必要字段'}), 400

    sql = "INSERT INTO period (start_date, end_date, flow, symptoms, mood, notes) VALUES (%s, %s, %s, %s, %s, %s)"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (start_date, end_date, flow, symptoms, mood, notes))
        conn.commit()
        return jsonify({'message': '经期数据保存成功'})
    finally:
        conn.close()
