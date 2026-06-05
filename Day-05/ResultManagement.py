from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI(
    title="Student Result Management System",
    description="Calculate SGPA,CGPA of the Student Result"
)

grade_points = {
    "O":10,
    "A+":9,
    "A":8,
    "B+":7,
    "B":6,
    "C":5,
    "F":0
}

students = []
student_id = 1

class PreviousSemester(BaseModel):
    semester: int
    sgpa: float
    credits:int

class Subject(BaseModel):
    subject: str
    grade: str
    credit: int

class StudentRequest(BaseModel):
    name: str
    roll_no: str
    current_semester: int
    previous_semesters: List[PreviousSemester] = []
    subjects: List[Subject]

def calculate_current_sgpa(subjects):
    total_credit_points = 0
    total_credits= 0

    for subject in subjects:
        grade = subject.grade.upper()

        if grade not in grade_points:
            raise HTTPException(status_code=400, detail = f"Invalid grade: {subject.grade}")
        
        if subject.credit <= 0:
            raise HTTPException(status_code=400, detail = "Credit must be grater than 0")
        
        point = grade_points[grade]
        credit_point = point * subject.credit

        total_credit_points += credit_point
        total_credits += subject.credit
    
    if total_credits == 0:
        raise HTTPException(status_code=400, detail = "Total credits cannot be zero")
    
    sgpa =  total_credit_points/total_credits

    return round(sgpa,2), total_credits, total_credit_points

def calculate_weighted_cgpa(previous_semesters, current_sgpa, current_credits):
    total_grade_points = 0
    total_credits = 0

    for sem in previous_semesters:

        # 1st semester case: no previous data
        if sem.semester == 0 and sem.sgpa == 0 and sem.credits == 0:
            continue

        if sem.sgpa < 0 or sem.sgpa > 10:
            raise HTTPException(status_code=400, detail="SGPA must be between 0 and 10")

        if sem.credits <= 0:
            raise HTTPException(status_code=400, detail="Semester credits must be greater than 0")

        total_grade_points += sem.sgpa * sem.credits
        total_credits += sem.credits

    total_grade_points += current_sgpa * current_credits
    total_credits += current_credits

    cgpa = total_grade_points / total_credits

    return round(cgpa, 2), total_credits

def calculate_average_cgpa(previous_semesters, current_sgpa):
    all_sgpas = []

    for sem in previous_semesters:

        # 1st semester case: no previous data
        if sem.semester == 0 and sem.sgpa == 0 and sem.credits == 0:
            continue

        all_sgpas.append(sem.sgpa)

    all_sgpas.append(current_sgpa)

    average_cgpa = sum(all_sgpas) / len(all_sgpas)

    return round(average_cgpa, 2)

def calculate_percentage(cgpa):
    return round(cgpa * 9.5, 2)

def get_remark(cgpa):
    if cgpa >= 9:
        return "Excellent"
    elif cgpa >= 8:
        return "Very Good"
    elif cgpa >= 7:
        return "Good"
    elif cgpa >= 6:
        return "Average"
    else:
        return "Needs Improvement"
    

@app.get("/")
def home():
    return{
        "message":"Welcome to Student Result Management System"
    }

@app.post("/students", status_code=201)
def add_student_result(student: StudentRequest):
    global student_id

    current_sgpa, current_credits, current_credit_points = calculate_current_sgpa(student.subjects)

    weighted_cgpa, total_credits_after_current_sem = calculate_weighted_cgpa(
        student.previous_semesters,
        current_sgpa,
        current_credits
    )

    average_cgpa = calculate_average_cgpa(
        student.previous_semesters,
        current_sgpa
    )

    percentage = calculate_percentage(weighted_cgpa)
    remark = get_remark(weighted_cgpa)

    result = {
        "id": student_id,
        "name": student.name,
        "roll_no": student.roll_no,
        "current_semester": student.current_semester,
        "previous_semesters": student.previous_semesters,
        "current_subjects": student.subjects,
        "current_semester_sgpa": current_sgpa,
        "current_semester_credits": current_credits,
        "current_semester_credit_points": current_credit_points,
        "weighted_cgpa": weighted_cgpa,
        "average_cgpa": average_cgpa,
        "total_credits_after_current_semester": total_credits_after_current_sem,
        "percentage": percentage,
        "remark": remark,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    students.append(result)
    student_id += 1

    return {
        "message" : "Student result calculated successfully",
        "student": result
    }

@app.get("/students")
def view_all_students():
    return {
        "total_students":len(students),
        "students":students
    }

@app.get("/students/{student_id}")
def view_student_by_id(student_id:int):
    for student in students:
        if student["id"] == student_id:
            return student
        
    raise HTTPException(status_code=404, detail = "Student Not Found")
