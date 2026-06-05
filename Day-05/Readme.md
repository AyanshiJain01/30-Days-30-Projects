# Day 05 - Student Result Management System API

## Project Overview

This is a Student SGPA and CGPA Calculator API built using FastAPI and Python.

The API calculates real SGPA using subject grades and credits. It also calculates CGPA using two methods:

1. **Weighted CGPA** based on semester credits
2. **Average CGPA** based on previous SGPAs

This project is part of my **30 Days 30 Real Projects Challenge**.

---

## Features

* Add student details
* Add current semester subjects
* Add grades and credits
* Convert grades into grade points
* Calculate real SGPA
* Calculate weighted CGPA
* Calculate average CGPA
* Calculate percentage
* Generate performance remark
* View all student results
* View student result by ID
* Created timestamp
* 404 error handling
* Swagger UI testing

---

## Tech Stack

* Python
* FastAPI
* Uvicorn
* Pydantic

---

## Grade Point Mapping

| Grade | Grade Point |
| ----- | ----------- |
| O     | 10          |
| A+    | 9           |
| A     | 8           |
| B+    | 7           |
| B     | 6           |
| C     | 5           |
| F     | 0           |

---

## Formula Used

### SGPA Formula

```text
SGPA = Total Credit Points / Total Credits
```

Where:

```text
Credit Point = Grade Point × Credit
```

### Weighted CGPA Formula

```text
Weighted CGPA =
(Previous Semester Grade Points + Current Semester Grade Points)
/
(Previous Semester Credits + Current Semester Credits)
```

### Average CGPA Formula

```text
Average CGPA =
Sum of all semester SGPAs / Number of semesters
```

### Percentage Formula

```text
Percentage = CGPA × 9.5
```

---

## Performance Remark Logic

| CGPA Range    | Remark            |
| ------------- | ----------------- |
| 9.0 and above | Excellent         |
| 8.0 - 8.99    | Very Good         |
| 7.0 - 7.99    | Good              |
| 6.0 - 6.99    | Average           |
| Below 6.0     | Needs Improvement |

---

## Installation

Install required packages:

```bash
pip install fastapi uvicorn
```

---

## Run the Project

```bash
uvicorn ResultManagement:app --reload
```

---

## Open Swagger UI

After running the server, open:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint                 | Description                                |
| ------ | ------------------------ | ------------------------------------------ |
| GET    | `/`                      | Home route                                 |
| POST   | `/students`              | Add student result and calculate SGPA/CGPA |
| GET    | `/students`              | View all student results                   |
| GET    | `/students/{student_id}` | View result by student ID                  |

---

## Sample Request Body

```json
{
  "name": "Ayanshi",
  "roll_no": "BTBTCS101",
  "current_semester": 1,
  "previous_semesters": [
    {
      "semester": 0,
      "sgpa": 0,
      "credits": 0
    }
  ],
  "subjects": [
    {
      "subject": "DSA",
      "grade": "A+",
      "credit": 4
    },
    {
      "subject": "DBMS",
      "grade": "A",
      "credit": 3
    }
  ]
}
```

---

## Note for First Semester Students

If the student is in the first semester and does not have previous semester data, use:


```json
"previous_semesters": [
  {
    "semester": 0,
    "sgpa": 0,
    "credits": 0
  }
]
```


---

## Sample Response

```json
{
  "message": "Student result calculated successfully",
  "student": {
    "id": 1,
    "name": "Ayanshi",
    "roll_no": "BTBTCS101",
    "current_semester": 1,
    "current_semester_sgpa": 8.57,
    "current_semester_credits": 7,
    "weighted_cgpa": 8.57,
    "average_cgpa": 8.57,
    "percentage": 81.42,
    "remark": "Very Good",
    "created_at": "2026-06-05 12:00:00"
  }
}
```

---

## Project Structure

```text
Day-05/
│
├── ResultManagement.py
└── README.md
```

---

## Learning Outcomes

Through this project, I learned:

* Building APIs using FastAPI
* Using Pydantic models
* Working with nested request bodies
* Converting grades into grade points
* Calculating real SGPA using credits
* Calculating weighted CGPA
* Calculating average CGPA
* Handling first semester cases
* Returning proper error messages
* Testing APIs using Swagger UI

---

## Future Improvements

* Store results in a database
* Add update and delete result APIs
* Add multiple student filtering
* Add authentication
* Export result as PDF
* Deploy the API

---

## Author

Ayanshi Jain

30 Days 30 Real Projects Challenge 🚀
