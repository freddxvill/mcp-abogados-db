import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from fastmcp import FastMCP

app = FastMCP("company-fredd-server")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port = int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME", "company_fredd"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        cursor_factory=RealDictCursor # retorna diccionarios en vez de tuplas
    )

@app.tool # sirve para marcar esta función como una herramienta que puede ser llamada por el modelo
def list_employees(limit: int = 5) -> List[Dict[str, Any]]:
    """Lista los empleados de la empresa, con un límite opcional. """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, position, department, salary, hire_date
                FROM employees
                ORDER BY id
                LIMIT %s
            """, (limit,)
            )
            rows = cursor.fetchall()
            employees = []

            for row in rows:
                employees.append({
                    "id": row["id"],
                    "name": row["name"],
                    "position": row["position"],
                    "department": row["department"],
                    "salary": float(row["salary"]),
                    "hire_date": str(row["hire_date"].isoformat()) if row["hire_date"] else None
                })
            
            return employees
        
    except Exception as e:
        return {
            "error": f"Error al obtener los empleados: {e}"
        }

    finally:
        conn.close() 


@app.tool
def add_employee(
    name: str, 
    position: str, 
    department: str, 
    salary: float, 
    hire_date: Optional[str] = None # fecha opcional, pero se espera que sea un string en formato ISO (YYYY-MM-DD)
    ) -> Dict[str, Any]:
    """Agrega un nuevo empleado a la base de datos. """
    try:
        if not name.strip():
            return {
                "error": "El nombre del empleado no puede estar vacío."
            }

        if salary <= 0:
            return {
                "error": "El salario debe ser mayor que cero."
            }
        
        if not hire_date:
            hire_date = datetime.now().strftime("%Y-%m-%d") # fecha actual en formato ISO

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO employees (name, position, department, salary, hire_date)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, name, position, department, salary, hire_date
            """, (name.strip(), position.strip(), department.strip(), salary, hire_date)
            )
            new_employee = cursor.fetchone()
            conn.commit()

            return {
                "success": True,
                "employee": {
                    "id": new_employee["id"],
                    "name": new_employee["name"],
                    "position": new_employee["position"],
                    "department": new_employee["department"],
                    "salary": float(new_employee["salary"]),
                    "hire_date": str(new_employee["hire_date"])
                }
            }
        
    except Exception as e:
        return {
            "error": f"Error al agregar el empleado: {e}"
        }

    finally:
        conn.close()

if __name__ == "__main__":
    app.run(transport="sse", host="0.0.0.0", port=3000)


