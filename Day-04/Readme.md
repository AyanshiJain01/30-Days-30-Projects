# Day 04 - URL Shortener API (Mini Bitly Clone)

## Project Overview

This project is a URL Shortener API built using FastAPI.

It converts long URLs into short and easy-to-share links. Users can either generate an automatic short code or provide their own custom short code. The API also tracks click counts, creation timestamps, and analytics for each shortened URL.

This project is part of my **30 Days 30 Real Projects Challenge**.

---

## Features

✅ Shorten long URLs
✅ Generate unique short codes automatically
✅ Create custom short codes
✅ Redirect users to the original URL
✅ View all shortened URLs
✅ Track click counts
✅ Store creation timestamps
✅ URL analytics endpoint
✅ Proper 404 error handling
✅ Interactive Swagger UI documentation

---

## Tech Stack

* Python
* FastAPI
* Uvicorn
* Pydantic

---

## Libraries Used

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from datetime import datetime
import random
import string
```

---

## Installation

Install the required packages:

```bash
pip install fastapi uvicorn
```

---

## Run the Project

```bash
uvicorn URLshortener:app --reload
```

---

## Open Swagger Documentation

After running the server, open:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint                | Description              |
| ------ | ----------------------- | ------------------------ |
| GET    | /home                   | Home Route               |
| POST   | /shorten                | Create Short URL         |
| GET    | /urls                   | View All URLs            |
| GET    | /analytics/{short_code} | View URL Analytics       |
| GET    | /{short_code}           | Redirect to Original URL |

---

## Example Request

### Create Short URL

```json
{
  "url": "https://www.linkedin.com/in/your-profile",
  "custom_code": "linkedin"
}
```

---

## Example Response

```json
{
  "message": "Short URL created successfully",
  "short_code": "linkedin",
  "short_url": "http://127.0.0.1:8000/linkedin"
}
```

---

## Analytics Example

```json
{
  "short_code": "linkedin",
  "original_url": "https://www.linkedin.com/in/your-profile",
  "short_url": "http://127.0.0.1:8000/linkedin",
  "clicks": 5,
  "created_at": "2026-06-04 10:00:00"
}
```

---

## Project Structure

```text
Day-04/
│
├── urlShortener.py
└── README.md
```

---

## Learning Outcomes

Through this project, I learned:

* Building REST APIs using FastAPI
* Request validation using Pydantic
* Working with dynamic routes
* Generating random short codes
* Implementing URL redirection
* Tracking analytics and click counts
* Handling errors using HTTPException
* Testing APIs with Swagger UI

---

## Future Improvements

* Database Integration (SQLite / PostgreSQL)
* User Authentication
* URL Expiration
* QR Code Generation
* Deployment on Render
* Custom Analytics Dashboard

---

## Author

Ayanshi Jain

30 Days 30 Real Projects Challenge 🚀
