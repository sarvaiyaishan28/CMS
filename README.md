# CMS

This project is role based Content Management System(CMS) using Django REST Framework(DRF).

## Installation

1. Clone the Git Repository
```bash
https://github.com/sarvaiyaishan28/CMS.git
```
2. Create a .env File

- Navigate to the project directory.
- Create a `.env` file and copy the content from the `env.example` file into it.
3. Ensure Docker is Installed

- Verify that Docker is installed on your system.
- If Docker is not installed, download and install it before proceeding.
4. Build the Project
- Use the following commands based on your operating system:
```bash
# For Windows
docker-compose build
```
```bash
# For Ubuntu
sudo docker-compose build
```
5. Start and Run the Project
- Start the application using the commands below:
```bash
# For Windows
docker-compose up
```
```bash
# For Ubuntu
sudo docker-compose up
```

## Create A User

#### Creating a Superuser
1. Access the Docker Container

- Run the following commands to enter the container shell:


```bash
# For Windows
docker exec -it cms_web_container /bin/bash
```
```bash
# For Ubuntu
sudo docker exec -it cms_web_container /bin/bash
```
2. Create the Superuser
- Execute the following command:
```bash
python manage.py createsuperuser
```
- Provide the following credentials:
```python
email : superadmin@gmail.com
password : Admin@123
```

## URL's
### 1. Admin panel
```bash
http://localhost:8000/admin/
``` 
### 2. API Document
```bash
http://localhost:8000/redoc/
```

## Run Test Cases

1. Access the Docker Container

- Run the following commands to enter the container shell:


```bash
# For Windows
docker exec -it cms_web_container /bin/bash
```
```bash
# For Ubuntu
sudo docker exec -it cms_web_container /bin/bash
```

2. Execute the following command:
```bash
python manage.py test
```