@jwt.post("/verifyToken")
async def check_token(payload: dict = Depends(jwt_dependencies.get_verified_payload)):
    return {"message": "Token verified", "payload": payload}
