# Employee Management API

## 📋 Overview
The **Employee Management API** is a RESTful API built using FastAPI to manage employee data. It supports CRUD operations, pagination, and additional features like filtering.

---

## 📌 Features
- **CRUD Operations**:
  - Create, Read, Update, and Delete employee records.
- **Pagination**:
  - Retrieve employees in paginated results.
- **Filtering**:
  - Filter employees by employee id.
- **Sorting**:
  - Sort employees by fields like salary (optional).
- **Error Handling**:
  - Proper HTTP status codes and error messages for invalid requests.

---

## 📦 Tech Stack
- **Framework**: FastAPI
- **Database**: MySQL
- **Environment Management**: Python-dotenv
- **Testing**: Pytest

---

## 📂 Endpoints

### CRUD Endpoints
| Method   | Endpoint               | Description                          |
|----------|-------------------------|--------------------------------------|
| `GET`    | `/employees`           | List all employees (with pagination) |
| `GET`    | `/employees/{id}`      | Get a single employee by ID          |
| `POST`   | `/employees`           | Create a new employee                |
| `PUT`    | `/employees/{id}`      | Update an existing employee          |
| `DELETE` | `/employees/{id}`      | Delete an employee                   |

### Query Parameters for Pagination
- `/employees?limit=10&offset=0`

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL
- `pip` (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/employee-management-api.git
   cd employee-management-api

2. Create a virtual environment:
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Set up the .env file: Create a .env file in the root directory with the following content:

    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=your username  
    DB_PASSWORD=your password
    DB_NAME=your database name
    TABLE_NAME=your table name

5. Run the application:
    uvicorn main:app --reload

6. Access the API:

    Swagger UI: http://127.0.0.1:8000/docs
    ReDoc: http://127.0.0.1:8000/redoc

7. Run frontend application
    streamlit run frontend.py

🧪 Testing
1. Install testing dependencies:
    pip install pytest

2. Run tests:
    pytest test_main.py

🚀 Example API Usage
Create an Employee
Request:

Response:

Get All Employees (Paginated)
Request:

POST /employees
{
  "name": "John Doe",
  "department": "Engineering",
  "salary": 60000,
  "join_date": "2023-01-01"
}

Response:

{
  "message": "Employee created successfully"
}

Get All Employees (Paginated)
Request:

GET /employees?limit=5&offset=0

Response:

{
  "employees": [
    {
      "id": 1,
      "name": "John Doe",
      "department": "Engineering",
      "salary": 60000,
      "join_date": "2023-01-01"
    },
    ...
  ]
}


🧠 Advanced Features to be cont.
Sorting:
    Add sorting functionality using query parameters (e.g., /employees?sort=salary).
Caching:
    Add caching for the GET /employees endpoint to improve performance.
Logging:
    Add logging for create, update, and delete operations.
Audit Logs:
    Track changes made to employee records (e.g., who made the change and when).
