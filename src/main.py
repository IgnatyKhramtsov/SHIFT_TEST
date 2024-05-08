import uvicorn
from fastapi import FastAPI
from user_auth.auth import router as router_auth
from user_auth.router import router as router_user


app = FastAPI(
    title='REST-сервис просмотра текущей зарплаты и даты следующего повышения.',
    docs_url='/',
)


app.include_router(router_auth)
app.include_router(router_user)

@app.get('/api/v1/ping', tags=["Main Page"])
def ping():
    return "Pong"


if __name__ == "__main__":
    uvicorn.run(f"main:app", port=8001, reload=True)