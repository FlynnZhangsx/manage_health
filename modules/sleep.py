# modules/sleep.py
from flask import Blueprint, request, jsonify, current_app
import pymysql

bp = Blueprint('sleep', __name__)

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
def record_sleep():
    data = request.get_json()
    date = data.get('date')
    sleep_time = data.get('sleepTime')
    wake_time = data.get('wakeTime')
    quality = data.get('quality')

    if not all([date, sleep_time, wake_time]):
        return jsonify({'error': '缺少必要字段'}), 400

    sql = "INSERT INTO sleep (date, sleep_time, wake_time, quality) VALUES (%s, %s, %s, %s)"

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (date, sleep_time, wake_time, quality))
        conn.commit()
        return jsonify({'message': '睡眠数据保存成功'})
    finally:
        conn.close()
