class JWTDependencies:
    #Funzione che controlla il token
    def get_verified_payload(
        self,
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
    ) -> Dict[str, Any]:
        service = JWTService()
        success, result = service.verify_token(credentials=credentials)
        if not success:
            raise HTTPException(status_code=401, detail=result["message"])
        return result

    #Funzione per il rilascio di un nuovo token
    def get_new_token(
        self,
        client_id: str = Form(...),
        client_secret: str = Form(...),
        session: Session = Depends(db_dependencies.get_session),
    ) -> Dict[str, Any]:
        service = JWTService(session=session)
        success, result = service.generate_token(
            client_id=client_id, client_secret=client_secret
        )
        if not success:
            raise HTTPException(status_code=401, detail=result["message"])
        return result