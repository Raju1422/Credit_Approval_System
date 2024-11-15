# **Credit Approval System**

A Django-based backend application to manage a credit approval system, including customer registration, loan eligibility checks, loan creation, and loan viewing functionalities. The application uses PostgreSQL for data storage and Docker for containerization.

---

## **Tech Stack**
- **Backend**: Django 4+, Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Dependencies Management**: pip and `requirements.txt`

---

## **Setup and Installation**

### **Prerequisites**
- Docker and Docker Compose installed on your system.
- Clone this repository:
  ```bash
  git clone https://github.com/Raju1422/Credit_Approval_System.git
  cd CreditApprovalSystem
  
## **Steps to Run the Application**
- Add  **.env**  file into the root directory 

#### **Build and Run the Containers**
 - Build and Run the Containers Use Docker Compose to build and start the containers:
 ```bash
 docker-compose up --build
````
#### **Run Migrations**
- Inside the running container, apply migrations:
```bash
docker-compose exec web python manage.py migrate
````
#### **Ingest Initial Data**
- Run management commands to  ingest data from customer_data.xlsx and loan_data.xlsx:

```bash 
## to insert customer data 
docker-compose exec web python manage.py insert_customers customer_data.xlsx
````
```bash 
## to insert loand data
docker-compose exec web python manage.py insert_loan_data loan_data.xlsx
```
#### Note : 
- I already ingested customer_data and loan_data into database .
#### **Access the Application**
- The application will be accessible at http://localhost:8000/.





