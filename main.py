from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def root():
  return {"message":"Hey ! made by Priyanshu"}

@app.get('/hello/{name}')
def hello(name):
  return f"Welcome {name}"

