# Foodboxes shop project with Django REST Framework on Stepik

Training project for [a course on the Stepik](<https://stepik.org/course/73594>).

Creating a backend REST API for online shop:
- Django Management Command for populating DB from external API;
- Media and static files support;
- function-based view for desired item;
- response for GET request with JSON data.

## Dependencies

All requirements are listed in the file: `requirements.txt`.

## Populate DB with initial data

Make and apply migrations for the project.
Execute django command `python manage.py load_data` to populate DB with initial data.
URL for initial data is hard-coded in the `load_data.py`.

## Interact with API

Response can be received on URL `api/v1/items/<integer>`.