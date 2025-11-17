@jwt.post("/token")
async def get_token(payload: dict = Depends(jwt_dependencies.get_new_token)):
    return payload
