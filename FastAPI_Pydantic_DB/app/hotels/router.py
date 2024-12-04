from fastapi import APIRouter, Depends
from app.hotels.schemas import SHotel, HotelList
from app.hotels.services_dao import HotelsDAO


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("")
async def get_all_hotels() -> list[SHotel]:
    return await HotelsDAO.find_all()


# @router.get("/search")
# async def get_hotels_by_filters(search_args: HotelSearchArg = Depends()) -> list[SHotel]:
#     # Конвертуємо `search_args` у словник
#     filter_dict = {key: value for key, value in vars(search_args).items() if value is not None}
#     return (await HotelsDAO.find_all(**filter_dict)


@router.get("/{location}")
async def get_hotels_by_name(location: HotelList = Depends()) -> list[SHotel]:
    hotels = await HotelsDAO.get_list_of_hotels(location)
    # Конвертуємо ORM-об'єкти в Pydantic-моделі
    # return [SHotel.from_orm(hotel) for hotel in hotels]
    # return [SHotel(**hotel) for hotel in hotels]
    # return hotels
    return [
        SHotel(
            **hotel['Hotels'].__dict__,
            rooms_left=hotel['rooms_left']
        )
        for hotel in hotels
    ]


@router.get("/id/{hotel_id}")
async def get_hotel_info_by_id(hotel_id: int) -> list[SHotel]:
    return await HotelsDAO.find_all(id=hotel_id)
