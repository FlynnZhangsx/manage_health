# modules/bmi.py
from flask import Blueprint, request, jsonify, current_app
import pymysql

bp = Blueprint('bmi', __name__)

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
def record_bmi():
    data = request.get_json()
    date = data.get('date')
    weight = data.get('weight')
    height = data.get('height')
    bmi_value = data.get('bmi_value')  # 前端可自行计算或在后端计算

    if not all([date, weight, height]):
        return jsonify({'error': '缺少必要字段'}), 400

    # 如果前端没有计算 bmi_value，则也可在此计算：BMI = weight / ((height/100)^2)
    if not bmi_value:
        try:
            bmi_value = weight / ((height / 100) ** 2)
        except Exception:
            return jsonify({'error': '计算 BMI 时出错'}), 400

    sql = "INSERT INTO bmi (date, weight, height, bmi_value) VALUES (%s, %s, %s, %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (date, weight, height, bmi_value))
        conn.commit()
        return jsonify({'message': 'BMI 数据保存成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
