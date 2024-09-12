# Importando as bibliotecas e modulos
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import csv

app = FastAPI()

auth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verifica_token(token: str):
    if token != "supersecreto":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {"usuario":"Natanael"}

@app.post("/token")
async def login():
    return {"access_token": "supersecreto", "tpken_type": "bearer"}
    

@app.get("/")
async def index(token: str = Depends(auth2_scheme)):
    usuario = verifica_token(token)
    return {"menssagem": "olá {usuario}"}

@app.get("/items/{item_id}")
async def ler_item(item_id: int, pesquisa: str):
    return {"ID do item:": item_id, "Caixa de pesquisa": pesquisa}

    
@app.get("/creditos/{idade}")
async def filtrar_por_idade(idade> int):
    
    lista =[]
    
    with open("datasets/credit_risk_dataset.csv") as arquivo:
        for linha in arquivo:
            if idade == linha[0]:
                lista.append({"leon_intent": linha[4]})
    
    return lista        
