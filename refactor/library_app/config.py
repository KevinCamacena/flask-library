from dotenv import dotenv_values

config = dotenv_values(".env")
URI = f"mysql+pymysql://{config['MYSQL_ROOT']}:{config['MYSQL_ROOT_PASSWORD']}@localhost:3306/{config['MYSQL_DATABASE']}"
print(URI)

class Config:
    SQLALCHEMY_DATABASE_URI = URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
