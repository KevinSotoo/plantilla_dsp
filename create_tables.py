import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

def init_db():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL no encontrada en las variables de entorno")

    engine = create_engine(database_url)
    try:
        print("Creando/verificando tablas en la base de datos (no sobrescribe existente)...")
        SQLModel.metadata.create_all(engine)
        print("¡Tablas creadas/verificadas exitosamente!")
    except Exception as e:
        print(f"Error al crear/verificar tablas en la base de datos: {e}")
        raise

if __name__ == "__main__":
    print("Iniciando verificación/creación de la base de datos...")
    init_db()
    print("¡Proceso completado!")