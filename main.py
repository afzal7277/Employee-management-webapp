from fastapi import FastAPI, HTTPException
from fastapi import Query
from typing import Optional
from pydantic import BaseModel
import mysql.connector.pooling
from mysql.connector import Error
from dotenv import load_dotenv
import os
app = FastAPI()

# Load environment variables from .env file
load_dotenv()

host=os.getenv("DB_HOST")
port=os.getenv("DB_PORT")
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
db_name=os.getenv("DB_NAME")
tb_name=os.getenv("TABLE_NAME")

# Create the connection pool
pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,
    host=host,
    port=port,
    user=user,
    password=password,
    database=db_name
)



def create_database_and_schema():
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {tb_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                department VARCHAR(255),
                salary INT,
                join_date DATE
            )
        """)
        print("Database and table setup complete.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

create_database_and_schema()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/employees")
def get_employees(limit: int = Query(10), offset: int = Query(0)):
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch employees with pagination
        cursor.execute(f"SELECT * FROM {tb_name} LIMIT %s OFFSET %s", (limit, offset))
        employees = cursor.fetchall()

        return {"employees": employees}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {tb_name} WHERE id = %s", (employee_id,))
        employee = cursor.fetchone()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"employee": employee}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

class Employee(BaseModel):
    name: str
    department: str
    salary: int
    join_date: str


@app.post("/employees")
def create_employee(employee: Employee):
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {tb_name} (name, department, salary, join_date) VALUES (%s, %s, %s, %s)",
            (employee.name, employee.department, employee.salary, employee.join_date)
        )
        conn.commit()
        return {"message": "Employee created successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[int] = None
    join_date: Optional[str] = None

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: UpdateEmployee):
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the employee exists
        cursor.execute(f"SELECT * FROM {tb_name} WHERE id = %s", (employee_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Employee not found")

        # Build the update query dynamically
        fields = []
        values = []
        if employee.name:
            fields.append("name = %s")
            values.append(employee.name)
        if employee.department:
            fields.append("department = %s")
            values.append(employee.department)
        if employee.salary:
            fields.append("salary = %s")
            values.append(employee.salary)
        if employee.join_date:
            fields.append("join_date = %s")
            values.append(employee.join_date)

        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        query = f"UPDATE {tb_name} SET {', '.join(fields)} WHERE id = %s"
        values.append(employee_id)

        # Execute the update query
        cursor.execute(query, tuple(values))
        conn.commit()
        return {"message": "Employee updated successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    try:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {tb_name} WHERE id = %s", (employee_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Employee not found")
        cursor.execute(f"DELETE FROM {tb_name} WHERE id = %s", (employee_id,))
        conn.commit()
        return {"message": "Employee deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
