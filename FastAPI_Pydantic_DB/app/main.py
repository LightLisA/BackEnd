from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.frontend.pages.router import router as router_pages
from fastapi.staticfiles import StaticFiles
from app.frontend.images.router import router as router_images

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
# Додаємо статичні файли
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")
app.include_router(router_images)

# add platforms which can call our API
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
