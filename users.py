from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#entidad user
class User(BaseModel):
    id : int
    name : str
    apellido : str
    url : str
    age : int

users_list = [User(id=1,name="Andres", apellido="Medina", url="https://moure.dev", age=25),
         User(id=2,name="Domi", apellido="Medina", url="https://moure.com", age=3),
         User(id=3,name="Dani", apellido="Medina", url="https://moure.co", age=26)]

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Andres", "surname": "Medina", "url":"https://moure.dev","age":25},
            {"name": "Domi", "surname": "Medina", "url":"https://moure.com","age":25},
            {"name": "Dani", "surname": "Medina", "url":"https://moure.co","age":25}]

@app.get("/users")
async  def users():
    return users_list

#path
@app.get(f"/user/{id}")
async  def user(id: int):
    users_new = filter(lambda user: user.id == id, users_list)
    try:
        return list(users_new)[0]
    except:
        return {"error": "No se ha encontrado usuario"}

#query
@app.get(f"/user/")
async  def user(id: int):
    return search_user(id)

def search_user(id: int):
    users_new = filter(lambda user: user.id == id, users_list)
    try:
        return list(users_new)[0]
    except:
        return {"error": "No se ha encontrado usuario"}

@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"Error" : "El usuario ya existe."}
    else:
        users_list.append(user)


