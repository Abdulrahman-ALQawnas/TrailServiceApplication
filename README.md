# TrailServiceApplication
The TrailService micro-service manages trail-related information, including trail details, waypoints, authors, and audit logs. It provides CRUD operations and integrates with an Authenticator API for user validation. This service is a core component of the Trail Application, enabling seamless data management and secure access.
# 1. Introduction
The TrailService micro-service manages trail-related information, including trail details, waypoints, authors, and audit logs. It provides CRUD operations and integrates with an Authenticator API for user validation. This service is a core component of the Trail Application, enabling seamless data management and secure access.
This document provides a detailed guide to the TrailService microservice. It starts by an description of what it is for, architecture, and primary functionalities, and then technical details regarding API endpoints, database schema design and strategies for integration. You'll also find instructions for deploying the service using containerized environments and orchestration platforms like Docker and Kubernetes. For developers and stakeholders, there is access in the service’s GitHub repository to source code and implementation information, as well as to the hosted microservice to observe it in use.

# 2. Database Design
The database was normalized to 3NF to eliminate redundancies and ensure data integrity. The following tables were created:

1. Trail: Stores trail details.
2. Waypoint: Holds latitude and longitude for trail waypoints.
3. Author: Maintains information about trail authors.
4. TrailLog: Records audit logs for trail modifications.
The ERD (Entity Relationship Diagram) illustrates the relationships between these tables. The Trail table has foreign key relationships with the Author and Waypoint tables, while the TrailLog table tracks changes.

# 3. Micro-Service Design
The TrailService micro-service provides a RESTful API for managing trail data. Below are the main design components:
- UML Class Diagram: Represents the classes, including Trail, Author, Waypoint, and TrailLog.
- Sequence Diagram: Shows workflows, such as creating a trail and fetching trail details.
- API Endpoints:

Method 
Endpoint 
Description 
GET 
/trails
Fetch all trails.      
POST 
/trails
 Create a new trail.   
PUT 
/trails/<id>
Update an existing trail
DELETE 
/trails/<id>
Delete a trail.                 
GET 
/waypoints/<id>    
 Fetch waypoints for a trail. 

# 4. Implementation
The micro-service was implemented in Flask and integrates with Microsoft SQL Server. Below are the key implementation components:
- Database Configuration:

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://username:password@server/TrailDB'
db = SQLAlchemy(app)


- Create Trail Endpoint:

@app.route('/trails', methods=['POST'])
def create_trail():
    data = request.get_json()
    user = authenticate_user(data['email'], data['password'])
    if not user:
        return {"message": "Authentication failed"}, 401
    
    new_trail = Trail(
        trailName=data['trailName'],
        trailDescription=data.get('trailDescription', ''),
        trailLength=data['trailLength'],
        trailDifficulty=data['trailDifficulty'],
        authorID=user['userID']
    )
    db.session.add(new_trail)
    db.session.commit()
    return {"message": "Trail created", "trailID": new_trail.trailID}, 201


# 5. Testing and Evaluation
Testing was conducted to verify that the micro-service met its functional and non-functional requirements.
1. Functional Testing:
- CRUD operations tested using Postman.
- Sample input/output verified for all endpoints.
2. Security Testing:
- SQL injection and role-based access control tested.
Strengths:
- Adheres to RESTful principles.
- Secure integration with the Authenticator API.
- Comprehensive audit logging.
Weaknesses:
- Limited automated testing.
- Basic error handling for edge cases.
Improvements:
- Introduce token-based authentication.
- Enhance error messages and validation.

# 6. Database Scripts
The following SQL scripts were used to create and populate the database:
- Create Tables:

CREATE TABLE Author (
    AuthorID INT PRIMARY KEY IDENTITY(1,1),
    Email VARCHAR(100) UNIQUE NOT NULL,
    Role VARCHAR(50) NOT NULL
);

CREATE TABLE Trail (
    TrailID INT PRIMARY KEY IDENTITY(1,1),
    Title VARCHAR(100) NOT NULL,
    Overview VARCHAR(500),
    Distance FLOAT,
    Complexity VARCHAR(50) NOT NULL,
    DateCreated DATETIME DEFAULT GETDATE(),
    AuthorID INT,
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID)
);
# LSEP (Legal, Social, Ethical, and Professional) Aspects
Legal, Social, Ethical, and Professional (LSEP) issues must be taken into account when creating the TrailService micro-service in order to guarantee regulatory compliance, safeguard users, and uphold professional standards. This paper describes the steps taken to resolve concerns about data integrity, security, privacy, and preservation.

## 1. Legal Considerations
### 1.1 Data Protection and Privacy
- Minimal data collection: Only essential user and trail information is stored.
- Anonymization: Sensitive data like passwords is stored in hashed form, and no personal data is publicly exposed.
- Access Control: Role-based access restrictions ensure that sensitive operations are protected.
### 1.2 Compliance with Intellectual Property
- Ensured data and APIs used are compliant with licensing and intellectual property laws.
## 2. Social Considerations
### 2.1 Accessibility
- Data is presented in JSON format, ensuring it is lightweight and compatible with assistive technologies.
- Trails can be accessed anonymously to encourage inclusivity.
### 2.2 Promoting Well-Being
- The application fosters outdoor activities to enhance users' physical and mental health.
## 3. Ethical Considerations
### 3.1 Ethical Use of Data
- Transparency: Users are informed of how their data is used.
- Purpose Limitation: Data is used solely for trail management and not for other purposes.
- Avoiding Bias: All trails and users are treated equally in the service.
### 3.2 Ethical Development Practices
- Open Collaboration: Code is hosted on GitHub for transparency and feedback.
- Testing for Bias: Ensured equal representation of all users' trails.
## 4. Professional Considerations
### 4.1 Security Measures
- Authentication: Integrated with the Authenticator API for secure login.
- Role-Based Access Control (RBAC): Restricted sensitive operations based on user roles.
- SQL Injection Prevention: Used parameterized queries to prevent attacks.
### 4.2 Integrity of Data
- Validation: Input data is validated at both the API and database levels.
- Transaction Management: Ensures data consistency during operations.
### 4.3 Preserving Data
- Backups: Assumed regular backups for disaster recovery.
- Audit Logs: Maintained logs for all trail-related activities.
## 5. Summary of Activities

Category
Activity
Example
Legal
Complying with GDPR and using minimal data.
Storing hashed passwords; avoiding plain text.		
Social
Promoting inclusivity and well-being.		
Allowing anonymous viewing of trails.
Ethical
Transparent and fair handling of user data
Informing users of data usage; avoiding prioritization.
Professional
Ensuring secure, consistent, and robust operations
Using 	RBAC, validating inputs, maintaining audit trails.	


# 5. Implementation
The TrailService micro-service was implemented using Python and Flask, with SQLAlchemy as the ORM to interact with the database. The service provides CRUD (Create, Read, Update, Delete) operations for managing trails and integrates with an external Authenticator API for user authentication. Below is an overview of the implementation steps.
## 5.1. Framework and Setup
The Flask framework was chosen for its simplicity and compatibility with RESTful API principles. SQLAlchemy was used to map Python classes to database tables, ensuring clean and efficient database operations.

 - Database Configuration: The database was hosted on Microsoft SQL Server, and connection details were configured using SQLAlchemy's connection string.
 - Authentication Integration: The Authenticator API was integrated via HTTP requests to validate user credentials.

# 6. Evaluation
## 6.1. Testing and Results
Testing was conducted to verify that the micro-service met its functional and non-functional requirements.

 1. Functional Testing:
 - Tested each CRUD endpoint using tools like Postman to ensure correct responses for valid and invalid requests.
 - Verified the integration with the Authenticator API to restrict access based on user credentials.
Test Example: Create Trail
- Input: JSON payload with trail details and user credentials.
 - Expected Output: HTTP 201 with a success message and trail ID.
 - Result: Passed.
Code Sample: Test Payload
json:
 {
 "email": "grace@plymouth.ac.uk",
 "password": "ISAD123!",
 "trailName": "Plymouth Waterfront",
 "trailLength": 5.0,
 "trailDifficulty": "Easy"
 }
 
## 6.2. Areas for Further Work
- Improving Authentication: Implementing token-based authentication (e.g., JWT) could further enhance security and scalability.
 - User Role Enhancements: Adding more granular roles or permissions could improve functionality.
 - Error Handling: Custom error messages and detailed logging could enhance the user and developer experience.
## 6.3. Reflection
Strengths:
 - The micro-service follows RESTful principles and is well-documented.
 - Adheres to security best practices, such as using parameterized queries and RBAC.
 - Successfully integrates with external APIs and SQL Server.

 Weaknesses:
 - Error handling could be more comprehensive, particularly for edge cases.
 - Limited automated testing was implemented due to time constraints.

 Improvements:
 - Incorporating unit tests using a framework like pytest or unittest would enhance code reliability.
 - Expanding Swagger documentation to include examples for all endpoints could improve developer usability.







