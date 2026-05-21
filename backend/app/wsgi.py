from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from app.core.config import DevConfig, ProdConfig
from app.core.extensions import db, migrate, cors, jwt, ma
from app.routes import (
    auth_bp,
    kitchen_bp,
    product_bp,
    recipe_bp,
    user_bp,
    ingredient_step_bp
)


def create_app(config_class=DevConfig):
    """Фабрика приложения Flask"""
    app = Flask(__name__)

    # Загрузка конфигурации
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    
    # CORS
    cors.init_app(
        app,
        origins=config_class.CORS_ORIGINS,
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # ====================== РЕГИСТРАЦИЯ BLUEPRINTS ======================
    app.register_blueprint(auth_bp)
    app.register_blueprint(kitchen_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ingredient_step_bp)

    # ====================== ГЛОБАЛЬНЫЕ ОБРАБОТЧИКИ ОШИБОК ======================

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error.description)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized", "message": "Authentication required"}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"error": "Forbidden", "message": "You don't have permission to access this resource"}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": "Something went wrong"}), 500

    # ====================== JWT CALLBACKS ======================

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "Token has expired",
            "message": "Please log in again"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "error": "Invalid token",
            "message": error
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "error": "Authorization required",
            "message": "Missing authorization token"
        }), 401

    # Тестовый маршрут
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "environment": "development" if app.config.get('DEBUG') else "production"
        }), 200

    return app


# Для запуска через python app/main.py
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)