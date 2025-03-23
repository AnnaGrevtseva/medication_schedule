from controllers.handlers import router
from fastapi import FastAPI

app = FastAPI(title='Расписание приема лекарств')
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
