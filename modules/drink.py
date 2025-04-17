# modules/drink.py
from flask import Blueprint, request, jsonify, current_app
import pymysql

bp = Blueprint('drink', __name__)

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
def record_drink():
    data = request.get_json()
    date = data.get('date')
    water_intake = data.get('water_intake')
    target = data.get('target')

    if not all([date, water_intake]):
        return jsonify({'error': '缺少必要字段'}), 400

    sql = "INSERT INTO drink (date, water_intake, target) VALUES (%s, %s, %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (date, water_intake, target))
        conn.commit()
        return jsonify({'message': '饮水记录保存成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
