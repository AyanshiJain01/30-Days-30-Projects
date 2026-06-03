# Day 03 - FastAPI Notes API with CRUD

## Project Overview

This is a simple Notes API built using FastAPI.

The API allows users to create, read, update, and delete notes using REST API endpoints. Each note contains a title, content, creation timestamp, and update timestamp.

This project is part of my **30 Days 30 Real Projects Challenge**, where I build one practical project every day to improve my development skills.

---

## Features

✅ Create a new note

✅ View all notes

✅ View a single note by ID

✅ Update an existing note

✅ Delete a note

✅ Automatically save creation date and time

✅ Automatically update modification date and time

✅ Proper 404 error handling

✅ Interactive API testing using Swagger UI

---

## Tech Stack

* Python
* FastAPI
* Uvicorn
* Pydantic

---

## Installation

Install the required packages:

```bash
pip install fastapi uvicorn
```

---

## Run the Project

Start the FastAPI server:

```bash
uvicorn notesAPI:app --reload
```

---

## Access Swagger Documentation

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides an interactive interface to test all API endpoints.

---

## API Endpoints

| Method | Endpoint         | Description       |
| ------ | ---------------- | ----------------- |
| GET    | /                | Home Route        |
| POST   | /notes           | Create a New Note |
| GET    | /notes           | View All Notes    |
| GET    | /notes/{note_id} | View Note by ID   |
| PUT    | /notes/{note_id} | Update Note by ID |
| DELETE | /notes/{note_id} | Delete Note by ID |

---

## Sample Request Body

```json
{
  "title": "FastAPI",
  "content": "Notes API using CRUD operations"
}
```

---

## Sample Response

```json
{
  "message": "Note Created Successfully",
  "note": {
    "id": 1,
    "title": "FastAPI",
    "content": "Notes API using CRUD operations",
    "created_at": "2026-06-03 12:00:00",
    "updated_at": null
  }
}
```

---

## Learning Outcomes

Through this project, I learned:

* Building REST APIs using FastAPI
* Implementing CRUD operations
* Creating request models using Pydantic
* Working with HTTP methods (GET, POST, PUT, DELETE)
* Handling errors using HTTPException
* Returning proper HTTP status codes
* Testing APIs using Swagger UI
* Managing timestamps using Python's datetime module

---

## Project Structure

```text
Day-03/
│
├── notesAPI.py
└── README.md
```

---

## Author

Ayanshi Jain

30 Days 30 Real Projects Challenge 🚀
