📋 Problem Statement
Build a small RESTful API to manage a company's employee data. The API should:

Store employee details in a relational database

Support CRUD operations

Allow filtering and pagination

Be tested with unit and integration tests

📌 Data Model

Employee:
- id (int, primary key)
- name (str)
- department (str)
- salary (int)
- join_date (date)

✅ Required Endpoints
Method	Endpoint	Description
GET	/employees	List all employees (with filter + pagination)
GET	/employees/{id}	Get single employee
POST	/employees	Create employee
PUT	/employees/{id}	Update employee
DELETE	/employees/{id}	Delete employee



⚙️ Stack Requirements
FastAPI or Django REST Framework

SQLite or PostgreSQL

SQLAlchemy or Django ORM

Pytest or unittest

Use an in-memory DB (for testing)




🚀 Example API Response
json
Copy
Edit
{
  "id": 1,
  "name": "Alice",
  "department": "Engineering",
  "salary": 85000,
  "join_date": "2023-03-15"
}





🧪 Test Cases to Include
✅ Test POST creates employee

✅ Test GET returns correct employee

✅ Test PUT updates salary

✅ Test DELETE removes employee

✅ Test pagination returns correct number of records







🧠 Bonus / Advanced Add-ons
Add caching for GET /employees

Add sorting (/employees?sort=salary)

Add logging for create/update/delete

Track audit logs (who made what change)