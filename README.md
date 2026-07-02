# GigHub API

GigHub API is a REST API developed using FastAPI to manage freelance gig listings.

## Features

- View all gigs
- Search gigs by title
- Filter gigs by category and budget
- View a gig by ID
- Create a new gig
- Update a gig
- Delete a gig

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn

## Running the API

Install the dependencies:
pip install fastapi uvicorn

Run the application:
uvicorn main:app --reload

Open Swagger UI:
http://127.0.0.1:8000/docs
