class Client(SQLModel, table=True):
    __tablename__ = "clients"
    id: int | None = Field(default=None, primary_key=True)
    client_id: str = Field(nullable=False, unique=True, index=True)
    client_secret: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime, server_default=func.now()),
    )
    is_active: bool = Field(default=True, sa_column=Column(Boolean, server_default="1"))
