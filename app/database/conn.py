from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

try:
    # Obtener valores de las variables de entorno
    host = os.getenv("HOST_DB")
    user_name = os.getenv("USERNAME_DB")
    password = os.getenv("PASSWORD_DB")
    database = os.getenv("DATABASE_NAME")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")  # Driver por defecto

    # Asegurarse de que las variables esenciales están presentes
    if not all([host, user_name, password, database]):
        raise ValueError("Faltan valores de variables de entorno esenciales")

    # Construir el URI de conexión para SQL Server
    URI = (
        f"mssql+pyodbc://{user_name}:{password}@{host}/{database}"
        f"?driver={driver}"
    )
    print(f"Conectando a la base de datos SQL Server...{URI}")

    # Crear el motor de SQLAlchemy
    engine = create_engine(URI)

    # Crear una base declarativa
    Base = declarative_base()

    # Configurar la sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Conexión a la base de datos SQL Server establecida correctamente.")

except Exception as e:
    print(f"Se produjo un error al conectar con la base de datos: {e}")
