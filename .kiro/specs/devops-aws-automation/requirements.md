# Requirements Document

## Introduction

This project involves designing and provisioning a multi-server Django-PostgreSQL application on AWS using Infrastructure as Code (Terraform), configuration management (Ansible), container orchestration (Docker Swarm), and automated CI/CD deployment. The system will consist of a Django web application with user authentication backed by PostgreSQL, deployed across multiple AWS EC2 instances in a Docker Swarm cluster with full automation.

## Requirements

### Requirement 1: Django Web Application

**User Story:** As a student, I want a Django web application with authentication functionality so that I can register, login, and access a personalized home page.

#### Acceptance Criteria

1. WHEN a user visits the application THEN the system SHALL redirect to the login page
2. WHEN a user accesses the login page THEN the system SHALL display username and password input fields
3. WHEN a user enters valid credentials (Roll No as username, Admission No as password) THEN the system SHALL authenticate against the PostgreSQL login table
4. WHEN authentication is successful THEN the system SHALL redirect to a home page displaying "Hello [username] How are you"
5. WHEN a user clicks logout THEN the system SHALL return to the login page
6. WHEN a user accesses the register page THEN the system SHALL allow creating new user records in the database
7. WHEN registration is submitted THEN the system SHALL store Roll No and Admission No in the login table

### Requirement 2: PostgreSQL Database Integration

**User Story:** As a system administrator, I want a PostgreSQL database to store user authentication data so that the Django application can authenticate users.

#### Acceptance Criteria

1. WHEN the system is deployed THEN PostgreSQL SHALL be running as a containerized service
2. WHEN the database is initialized THEN it SHALL contain a database named "postgres"
3. WHEN the database is created THEN it SHALL have a "login" table with username and password columns
4. WHEN the application starts THEN the login table SHALL be initially empty
5. WHEN users register THEN their credentials SHALL be stored in the login table
6. WHEN users authenticate THEN the system SHALL query the login table for validation

### Requirement 3: AWS Infrastructure Provisioning

**User Story:** As a DevOps engineer, I want AWS infrastructure provisioned using Terraform so that I have a scalable and reproducible cloud environment.

#### Acceptance Criteria

1. WHEN Terraform is executed THEN it SHALL create 4 t2.micro EC2 instances (free-tier eligible)
2. WHEN instances are created THEN each SHALL have an associated Elastic IP for static public access
3. WHEN infrastructure is provisioned THEN it SHALL include: Controller, Swarm Manager, Swarm Worker A, and Swarm Worker B
4. WHEN security groups are created THEN they SHALL allow HTTP/HTTPS/SSH and required custom ports
5. WHEN keypairs are generated THEN Terraform SHALL auto-generate and save the private key locally
6. WHEN Terraform completes THEN it SHALL output all public IP addresses

### Requirement 4: Server Configuration with Ansible

**User Story:** As a DevOps engineer, I want servers configured automatically using Ansible so that Docker Swarm can be deployed consistently.

#### Acceptance Criteria

1. WHEN Ansible playbooks run THEN they SHALL install Docker and Docker Compose on all nodes
2. WHEN the Swarm Manager is configured THEN it SHALL initialize the Docker Swarm cluster
3. WHEN Worker nodes are configured THEN they SHALL join the Swarm cluster automatically
4. WHEN services are deployed THEN Ansible SHALL use docker stack deploy with docker-compose.yml
5. WHEN inventory is used THEN it SHALL reference the Elastic IP addresses from Terraform

### Requirement 5: Docker Swarm Orchestration

**User Story:** As a system architect, I want containerized services orchestrated with Docker Swarm so that the application is highly available and scalable.

#### Acceptance Criteria

1. WHEN Docker images are built THEN there SHALL be separate images for Django web and PostgreSQL database
2. WHEN services are deployed THEN the web service SHALL run with at least 2 replicas
3. WHEN the database service is deployed THEN it SHALL use Docker volumes for data persistence
4. WHEN services communicate THEN they SHALL use overlay networks and service discovery by name
5. WHEN the stack is deployed THEN it SHALL be accessible via the Swarm Manager and Worker node IPs

### Requirement 6: CI/CD Pipeline Automation

**User Story:** As a developer, I want automated CI/CD pipelines so that code changes are automatically tested and deployed.

#### Acceptance Criteria

1. WHEN code is pushed to GitHub THEN the CI/CD pipeline SHALL trigger automatically
2. WHEN the pipeline runs THEN it SHALL build Docker images and deploy to the Swarm cluster
3. WHEN using Jenkins THEN it SHALL use Jenkinsfile with declarative syntax
4. WHEN using GitHub Actions THEN it SHALL use workflow YAML files
5. WHEN credentials are needed THEN they SHALL be stored securely in the CI system
6. WHEN deployment completes THEN the application SHALL be accessible on the Swarm cluster

### Requirement 7: Bootstrap Automation

**User Story:** As a DevOps engineer, I want a single script to provision the entire infrastructure so that deployment is fully automated.

#### Acceptance Criteria

1. WHEN bootstrap.sh is executed THEN it SHALL run terraform init and terraform apply automatically
2. WHEN Terraform completes THEN the script SHALL upload the generated PEM key to the workspace
3. WHEN infrastructure is ready THEN the script SHALL execute Ansible playbooks for configuration
4. WHEN Ansible completes THEN the script SHALL deploy the Docker stack
5. WHEN deployment finishes THEN the script SHALL trigger the initial CI/CD pipeline run

### Requirement 8: Project Structure and Organization

**User Story:** As a team member, I want a well-organized project structure so that all components are easily maintainable.

#### Acceptance Criteria

1. WHEN the project is structured THEN it SHALL have separate directories for terraform/, ansible/, docker/, django_app/, scripts/, and ci/
2. WHEN Terraform files are organized THEN they SHALL include all HCL files and key generation logic
3. WHEN Ansible files are organized THEN they SHALL include inventory, playbooks, and roles
4. WHEN Docker files are organized THEN they SHALL include Dockerfiles and docker-compose.yml
5. WHEN CI files are organized THEN they SHALL include GitHub Actions YAML or Jenkinsfile
6. WHEN the project is complete THEN it SHALL be pushed to a branch named with the student's Roll No

### Requirement 9: Testing and Validation

**User Story:** As a quality assurance engineer, I want automated tests to validate the application functionality so that deployments are reliable.

#### Acceptance Criteria

1. WHEN Selenium tests are provided THEN they SHALL validate the login/register/home/logout workflow
2. WHEN tests run THEN they SHALL verify database connectivity and data persistence
3. WHEN the application is deployed THEN it SHALL be accessible via all Swarm node public IPs
4. WHEN services are scaled THEN the application SHALL remain available during scaling operations
5. WHEN nodes are drained THEN the application SHALL continue serving requests from remaining nodes