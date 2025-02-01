import psycopg2

def test_connection():
    try:
        # Parámetros de conexión
        conn = psycopg2.connect(
            dbname="erp_sofrbusiness_dev",
            user="postgres",
            password="45dfs43Q244_dU@",
            host="149.130.183.87",
            port="5432"
        )
        print("✅ Conexión exitosa a la base de datos.")
        conn.close()
    except psycopg2.OperationalError as e:
        print("❌ Error de conexión:", e)
    except Exception as ex:
        print("⚠️ Error inesperado:", ex)

if __name__ == "__main__":
    test_connection()
