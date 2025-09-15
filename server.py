import os
import logging
import aiofiles
from aiohttp import web

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # cartella del progetto
VIDEO_DIR = os.path.join(BASE_DIR, 'images')          # cartella dei video

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PepperServer")

# --- MIDDLEWARE LOG ---
@web.middleware
async def log_middleware(request, handler):
    logger.info(f"📌 {request.method} {request.path}")
    try:
        response = await handler(request)
        logger.info(f"✅ {request.method} {request.path} -> {response.status}")
        return response
    except Exception as e:
        logger.error(f"❌ {request.method} {request.path} ERROR: {e}")
        raise

# --- HANDLER VIDEO CON RANGE ---
async def video_handler(request):
    filename = request.match_info['filename']
    path = os.path.join(VIDEO_DIR, filename)
    if not os.path.exists(path):
        raise web.HTTPNotFound()

    file_size = os.path.getsize(path)
    range_header = request.headers.get('Range', None)
    start, end = 0, file_size - 1

    if range_header:
        # "bytes=start-end"
        match = range_header.replace('bytes=', '').split('-')
        if match[0]:
            start = int(match[0])
        if len(match) > 1 and match[1]:
            end = int(match[1])
        end = min(end, file_size - 1)

    length = end - start + 1
    headers = {
        "Content-Type": "video/mp4",
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(length)
    }

    async with aiofiles.open(path, 'rb') as f:
        await f.seek(start)
        data = await f.read(length)
    status = 206 if range_header else 200
    return web.Response(body=data, status=status, headers=headers)

# --- CREA APP ---
app = web.Application(middlewares=[log_middleware])

# Serve tutti i file statici tranne i video
app.add_routes([web.static('/', BASE_DIR, show_index=True)])
# Route dedicata ai video
app.router.add_get('/images/{filename}', video_handler)

# --- RUN SERVER ---
if __name__ == "__main__":
    web.run_app(app, host='0.0.0.0', port=8000)
