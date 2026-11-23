from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "hello world"}

@app.get("/about")
def about():
    return {"message" :"welcome home"}
def load_data():
    with open("patients.json","r") as f :
        data = json.load(f)
    return data
@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patient(patient_id:str=Path(...,description='ID of the patient in the DB', example='P001')):
    #load all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get("/sort")
def sort(sort_by:str=Query(...,description="sort on the basis of height,weight,bmi"), order:str=Query(...,description="sort in ascending or descending ")):

        valid_fields = ["height","weight","bmi"]

        if sort_by not in valid_fields:
             raise HTTPException(status_code=401,detail=f"not valid query from {valid_fields}")

        if order not in ['asc','desc']:
             raise HTTPException(status_code=400,detail="invalid order")

        data = load_data()
        sort_order = True if order =="desc" else False
        sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse = sort_order)

        return sorted_data


        
     