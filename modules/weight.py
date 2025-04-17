# modules/weight.py
from flask import Blueprint, request, jsonify, current_app
import pymysql

bp = Blueprint('weight', __name__)

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
def record_weight():
    data = request.get_json()
    date = data.get('date')
    current_weight = data.get('current_weight')
    target_weight = data.get('target_weight')
    body_fat_rate = data.get('body_fat_rate')

    if not all([date, current_weight]):
        return jsonify({'error': '缺少必要字段'}), 400

    sql = "INSERT INTO weight (date, current_weight, target_weight, body_fat_rate) VALUES (%s, %s, %s, %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (date, current_weight, target_weight, body_fat_rate))
        conn.commit()
        return jsonify({'message': '体重数据保存成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
