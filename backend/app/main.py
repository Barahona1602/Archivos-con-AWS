# API imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local imports
from app.routes import routeHT4
from app.routes import routerCommand
from app.routes import routerAccess
# fastapi
app = FastAPI ()


app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# Routes
app.include_router(routerCommand.router)
app.include_router(routerAccess.router)
# app.include_router(routeHT4.router)


# if __name__ == "__main__":
#   import uvicorn
#   uvicorn.run(app, host="0.0.0.0", port=8000)