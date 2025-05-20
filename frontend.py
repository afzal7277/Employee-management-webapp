import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Employee Management Portal")

# --- Create Employee ---
st.header("Add New Employee")
with st.form("create_employee"):
    name = st.text_input("Name")
    department = st.text_input("Department")
    salary = st.number_input("Salary", min_value=0)
    join_date = st.date_input("Join Date")
    submitted = st.form_submit_button("Add Employee")
    if submitted:
        resp = requests.post(
            f"{API_URL}/employees",
            json={
                "name": name,
                "department": department,
                "salary": salary,
                "join_date": str(join_date)
            }
        )
        if resp.status_code == 200:
            st.success("Employee created successfully!")
        else:
            st.error(resp.json().get("detail", "Error occurred"))

# --- List Employees with Pagination ---
st.header("Employee List")
limit = st.number_input("Limit", min_value=1, value=5)
offset = st.number_input("Offset", min_value=0, value=0)
if st.button("Refresh List"):
    pass  # Just to trigger rerun

resp = requests.get(f"{API_URL}/employees?limit={limit}&offset={offset}")
if resp.status_code == 200:
    employees = resp.json()["employees"]
    for emp in employees:
        st.write(f"**ID:** {emp['id']} | **Name:** {emp['name']} | **Department:** {emp['department']} | **Salary:** {emp['salary']} | **Join Date:** {emp['join_date']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Edit {emp['id']}"):
                st.session_state['edit_id'] = emp['id']
        with col2:
            if st.button(f"Delete {emp['id']}"):
                del_resp = requests.delete(f"{API_URL}/employees/{emp['id']}")
                if del_resp.status_code == 200:
                    st.success("Deleted successfully!")
                else:
                    st.error(del_resp.json().get("detail", "Delete failed"))
                st.rerun()
else:
    st.error("Could not fetch employees.")

# --- Edit Employee ---
if 'edit_id' in st.session_state:
    emp_id = st.session_state['edit_id']
    st.header(f"Edit Employee ID {emp_id}")
    emp_resp = requests.get(f"{API_URL}/employees/{emp_id}")
    if emp_resp.status_code == 200:
        emp = emp_resp.json()["employee"]
        with st.form("edit_employee"):
            name = st.text_input("Name", value=emp["name"])
            department = st.text_input("Department", value=emp["department"])
            salary = st.number_input("Salary", min_value=0, value=emp["salary"])
            join_date = st.text_input("Join Date", value=emp["join_date"])
            submitted = st.form_submit_button("Update Employee")
            if submitted:
                update_resp = requests.put(
                    f"{API_URL}/employees/{emp_id}",
                    json={
                        "name": name,
                        "department": department,
                        "salary": salary,
                        "join_date": join_date
                    }
                )
                if update_resp.status_code == 200:
                    st.success("Employee updated successfully!")
                    del st.session_state['edit_id']
                    st.rerun()
                else:
                    st.error(update_resp.json().get("detail", "Update failed"))
    else:
        st.error("Employee not found.")