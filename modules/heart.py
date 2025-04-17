# modules/heart.py
from flask import Blueprint, request, jsonify, current_app
import pymysql

bp = Blueprint('heart', __name__)

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
def record_heart():
    data = request.get_json()
    date = data.get('date')
    average_rate = data.get('average_rate')

    if not all([date, average_rate]):
        return jsonify({'error': '缺少必要字段'}), 400

    sql = "INSERT INTO heart (date, average_rate) VALUES (%s, %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (date, average_rate))
        conn.commit()
        return jsonify({'message': '心率数据保存成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
