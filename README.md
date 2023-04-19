# DRF-Image-API
API project using django rest framework

## Installation
The project includes a requiremnts.txt file that installs all required libraries
```bash
pip install -r requirements.txt
```

Run the project with the command
```bash
python image_api/manage.py runserver
```
The project also include the Dockerfile and docker-compose files required to run the application via docker.

## User authorization
For proper operation of the api, user authorization is required imitating a logged in session. To do this, you must create an authentication token for a specific user
```bash
python image_api/manage.py drf_create_token <<username>> 
```
The generated token should be placed in the headers of the browser. From now on, it will be possible to use the api endpoints

## Endpoints
Three main urlpatters have been defined in the project:
  * admin/        - endpoint transferring us to the admin interface
  * image_api/    - endpoint moving to the default basic root view for DefaultRouter for iamges (supporting endpoint for images)
  * account_api/  - endpoint moving to the default basic root view for DefaultRouter for accoutns (supporting endpoint for accounts)
