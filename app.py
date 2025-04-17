# app.py
from flask import Flask
from config import Config
from modules import exercise, sleep, period, weight, bmi, drink, heart
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='frontend')  # 静态资源放在 frontend 文件夹
    app.config.from_object(Config)
    CORS(app)  # 允许跨域请求
    # 注册蓝图
    app.register_blueprint(exercise.bp, url_prefix='/exercise')
    app.register_blueprint(sleep.bp, url_prefix='/sleep')
    app.register_blueprint(period.bp, url_prefix='/period')
    app.register_blueprint(weight.bp, url_prefix='/weight')
    app.register_blueprint(bmi.bp, url_prefix='/bmi')
    app.register_blueprint(drink.bp, url_prefix='/drink')
    app.register_blueprint(heart.bp, url_prefix='/heart')

    # 如果希望同时提供前端文件服务，可加入：
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
