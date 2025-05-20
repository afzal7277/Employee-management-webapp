from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_employee():
    response = client.post(
        "/employees",
        json={
            "name": "John Doe",
            "department": "Engineering",
            "salary": 60000,
            "join_date": "2023-01-01"
        }
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Employee created successfully"
    
def test_get_employee():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["employee"]["name"] == "John Doe"

def test_update_employee():
    response = client.put(
        "/employees/1",
        json={"salary": 70000}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Employee updated successfully"

def test_delete_employee():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee deleted successfully"

def test_pagination():
    # Add multiple employees for pagination
    for i in range(10):
        client.post(
            "/employees",
            json={
                "name": f"Employee {i}",
                "department": "HR",
                "salary": 50000 + i * 1000,
                "join_date": "2023-01-01"
            }
        )

    # Test pagination with limit=5 and offset=0
    response = client.get("/employees?limit=5&offset=0")
    assert response.status_code == 200
    employees = response.json()["employees"]
    assert len(employees) == 5
    assert employees[0]["name"] == "Employee 0"
    assert employees[4]["name"] == "Employee 4"

    # Test pagination with limit=5 and offset=5
    response = client.get("/employees?limit=5&offset=5")
    assert response.status_code == 200
    employees = response.json()["employees"]
    assert len(employees) == 5
    assert employees[0]["name"] == "Employee 5"
    assert employees[4]["name"] == "Employee 9"
    
    
