import uvicorn
from fastapi import FastAPI
from user_auth.auth import router as router_auth
from user_auth.router import router as router_user
from salary.router import router as router_salary


app = FastAPI(
    title='REST-сервис просмотра текущей зарплаты и даты следующего повышения.',
    docs_url='/',
)


app.include_router(router_auth)
# app.include_router(router_user)
app.include_router(router_salary)

@app.get('/api/v1/ping', tags=["Ping"])
def ping():
    return "Pong"


if __name__ == "__main__":
    uvicorn.run(f"main:app", port=8001, reload=True)
