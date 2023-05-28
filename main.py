import asyncio
import uvicorn

async def start_application():
    from schedule.asgi import application
    await application(scope, receive, send)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_application())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
