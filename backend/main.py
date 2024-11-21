from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/medicines")
def get_all_meds():
    with open('data.json') as meds:
        data = json.load(meds)
    return data

@app.get("/medicines/{name}")
def get_single_med(name: str):
    with open('data.json') as meds:
        data = json.load(meds)
        for med in data["medicines"]:
            if med['name'] == name:
                return med
    return {"error": "Medicine not found"}

@app.post("/create")
def create_med(name: str = Form(...), price: float = Form(...)):
    with open('data.json', 'r+') as meds:
        current_db = json.load(meds)
        new_med = {"name": name, "price": price}
        current_db["medicines"].append(new_med)
        meds.seek(0)
        json.dump(current_db, meds)
        meds.truncate()
    return {"message": f"Medicine created successfully with name: {name}"}

@app.post("/update")
def update_med(name: str = Form(...), price: float = Form(...)):
    with open('data.json', 'r+') as meds:
        current_db = json.load(meds)
        for med in current_db["medicines"]:
            if med['name'] == name:
                med['price'] = price
                meds.seek(0)
                json.dump(current_db, meds)
                meds.truncate()
                return {"message": f"Medicine updated successfully with name: {name}"}
    return {"error": "Medicine not found"}

@app.delete("/delete")
def delete_med(name: str = Form(...)):
    with open('data.json', 'r+') as meds:
        current_db = json.load(meds)
        for med in current_db["medicines"]:
            if med['name'] == name:
                current_db["medicines"].remove(med)
                meds.seek(0)
                json.dump(current_db, meds)
                meds.truncate()
                return {"message": f"Medicine deleted successfully with name: {name}"}
    return {"error": "Medicine not found"}

@app.get("/average")
def get_average_price():
    with open('data.json') as meds:
        data = json.load(meds)
        medicines = [med for med in data["medicines"] if med.get("price") is not None]
        if not medicines:
            return {"average_price": 0}
        total_price = sum(med["price"] for med in medicines)
        avg_price = total_price / len(medicines)
    return {"average_price": round(avg_price, 2)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
