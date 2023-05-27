import asyncio
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim


async def get_postal_location(postal_code: int):
    async with Nominatim(
            user_agent='get_postal_location{}'.format(postal_code),
            adapter_factory=AioHTTPAdapter
    ) as geolocator:
        location = await geolocator.geocode({
            'country': 'USA',
            'postalcode': postal_code
        }, addressdetails=True)
        state = location.raw.get('address').get('state')
        return state


# async def get_random_position(location_city: str):
#     async with Nominatim(
#             user_agent='get_random_position{}'.format(location_city),
#             adapter_factory=AioHTTPAdapter
#     ) as geolocator:
#         location = await geolocator.geocode({
#             'country': 'USA',
#             'town': location_city
#         }, addressdetails=True)
#         city = location.raw
#         return city


# def main():
#     result = asyncio.run(get_postal_location('00601'))
#     return result

#
#
# print(main())

# def main():
#     result = asyncio.run(get_random_position('Adjuntas'))
#     return result
#
#
#
# print(main())
