# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://flask_user:flask_password_secure123@mysql:3306/channels_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-super-secret-jwt-key-change-in-production"
