import json
import os

from aiohttp import web, ClientSession

HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 8000))
DATA_FILENAME = os.environ.get('DATA_FILENAME', r'data.json')
BITOP = {
    'URL': os.environ.get('BITOP_URL'),
    'TOKEN': os.environ.get('BITOP_TOKEN'),
}


def response_error(exception: Exception, status=500):
    json_data = {
        'type': "Internal Server Error",
        'error': f'{exception.__class__.__name__}: {exception}',
        'description': '',
    }
    return web.json_response(json_data, status=status, )


async def get_data(request: web.Request):
    try:
        with open(DATA_FILENAME, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            return web.json_response(json_data)
    except json.decoder.JSONDecodeError as e:
        return response_error(e)


async def bitop_handler(request: web.Request):
    kwargs = dict(
        method=request.method,
        url='/' + request.match_info['tail'],
        data=await request.text(),
    )
    async with ClientSession(BITOP['URL'], headers={'x-bb-token': BITOP['TOKEN']}) as session:
        async with session.request(**kwargs) as response:
            return web.json_response(
                await response.json(),
                status=response.status,
            )


def main():
    app = web.Application()
    app.router.add_get('/data', get_data)
    app.router.add_route('*', '/bitop/{tail:.+}', bitop_handler)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
