from fastapi import FastAPI, Request, Form,Depends
import sqlite3

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel



#Connecting the database
conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

app = FastAPI()

#Connecting to HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


#Prints all the users
cursor.execute("SELECT * FROM jobs")
rows = cursor.fetchall()
cursor.execute("SELECT * FROM users")
userRows = cursor.fetchall()
def remove(string): 
    return string.replace(" ", "") 


@app.get("/")
async def root(request: Request):
    return "hi"
"""
@app.get("/allfiles/{item_id}")
async def read_items():
    item=[]
    for row in rows:
        item.append(row[0])
  
    return item
"""


@app.get("/items/{itemCall}/")
def form_to(request: Request,itemCall:str):
    skillsDict={}
    for row in rows:
        print(remove(row[0]))
        if itemCall.lower()==remove(row[0].lower()):
            res=row
            skills=res[4].split(", ")
            for i in range(len(skills)):
                skillsDict["skill"+str(i)]=skills[i]
                print(skillsDict["skill"+str(i)])

    myDict={"request": request, "item": itemCall,"company":res[0].upper(),"jobTitle":res[1].upper(),"jobSummary":res[2],"skills":res[4],"location":res[5]}   
    myDict.update(skillsDict)
    #Adds all the skills one by one, each can be accessed with skill0 or skill1 etc.
    
    print(myDict["skill1"])
    return templates.TemplateResponse('index.html',myDict)

currentUser=[]
@app.post("/items/")    #("/items/{itemCall}/")
def form_post(request: Request,num: int = Form(...)): #itemCall:str
    for user in userRows:
        if user[6]==num:
            print(user)
            currentUser=user
            return templates.TemplateResponse('login.html', context={'request': request,"welcome":user[0],"email":user[1],"skills":user[3],"field":user[5]})
        else:
            return "I'm sorry, but the login information was incorrect. Access Denied."


@app.get("/home")
def go_home(request:Request):
    myDict={"request": request,"user":currentUser}
    return (templates.TemplateResponse('home.html',myDict))