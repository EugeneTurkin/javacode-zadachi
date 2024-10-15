import aiohttp


async def rq(curr):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.exchangerate-api.com/v4/latest/{curr}') as response:
            html = await response.text()

        return html


# usage: uvicorn currency_function:app
async def app(scope, receive, send):
    if scope['method'] == 'GET':
        currency = scope["path"].lstrip("")
        b = await rq(currency)
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [('Content-Type', 'text/plain')]
        })
        await send({
            'type': 'http.response.body',
            'body': b.encode(),
        })
