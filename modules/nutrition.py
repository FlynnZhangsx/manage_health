# modules/nutrition.py
from flask import Blueprint, request, jsonify
import mysql.connector
from config import Config

bp = Blueprint('nutrition', __name__)

@bp.route('/log', methods=['POST'])
def log_nutrition():
    # 记录营养摄入
    data = request.json
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO nutrition (date, food_name, calories, protein, carbs, fat, meal_type) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (data['date'], data['food_name'], data['calories'], 
         data['protein'], data['carbs'], data['fat'], data['meal_type'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Nutrition logged successfully'})

@bp.route('/summary/<date>', methods=['GET'])
def get_nutrition_summary(date):
    # 获取每日营养摄入总结
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        'SELECT SUM(calories) as total_calories, '
        'SUM(protein) as total_protein, '
        'SUM(carbs) as total_carbs, '
        'SUM(fat) as total_fat '
        'FROM nutrition WHERE date = %s',
        (date,)
    )
    summary = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(summary)