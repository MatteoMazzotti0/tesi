#Import necessari
from fastapi import APIRouter, Depends

from app.dependencies.jwt.jwt_dependencies import jwt_dependencies

#Definizione di un router API
jwt = APIRouter() 
#Rotta API per verificare il token
@jwt.post("/verifyToken")
async def check_token(payload: dict = Depends(jwt_dependencies.get_verified_payload)):
    return {"message": "Token verified", "payload": payload}
#Rotta API per ottenere un nuovo token
@jwt.post("/token")
async def get_token(payload: dict = Depends(jwt_dependencies.get_new_token)):
    return payload
