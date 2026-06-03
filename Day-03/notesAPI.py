from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI (
    title = "NotesAPI",
    description = "Simple Notes API with CRUD Operations in FastAPI"
)

class NoteCreate(BaseModel):
    title:str
    content:str

class NoteUpdate(BaseModel):
    title: str
    content:str

notes = []
note_id = 1

#Now we are going to create our features----

#HOME
@app.get("/")
def home():
    return{
        "message" : "Welcome to Notes API"
    }


# Feature 1 -> Create a note
# for this we are using "POST" Method

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    global note_id

    new_note = {
        "id" : note_id,
        "title" : note.title,
        "content" : note.content,
        "created_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at" : None
    }

    notes.append(new_note)
    note_id += 1

    return{
        "message" : "Note Created Successfully",
        "note" : new_note
    }


# Feature 2 -> View all notes
#for this we are using "GET" Method

@app.get("/notes")
def view_note():
    return{
        "total_notes" : len(notes),
        "notes" : notes
    }

# Feature 3 -> View single note by id
#for this we are using "GET" Method

@app.get("/notes/{note_id}")
def get_note_by_id(note_id : int):
    for note in notes:
        if note["id"] == note_id:
            return note
        
    raise HTTPException(status_code=404, detail = "Note not found")

# Feature 4 -> Update a note
#for thiswe are using "PUT" Method

@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: NoteUpdate):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = updated_note.title
            note["content"] = updated_note.content
            note["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return{
                "message" : "Note updated successfully",
                "note" : note
            }
    raise HTTPException(status_code=404, detail="Note not found")

# Feature 5 -> Delete a note
#for thiswe are using "DELETE" Method

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return {
                "message" : "Note Deleted Successfully!!"
            }
    raise HTTPException(status_code=404, detail = "Note not found")

