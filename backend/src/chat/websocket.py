from fastapi import WebSocket
from typing import List


active_connections: List[WebSocket] = []  # Для отслеживания активных соединений


# Функция для подключения WebSocket
async def connect_to_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)


# Функция для отключения WebSocket
async def disconnect_from_websocket(websocket: WebSocket):
    active_connections.remove(websocket)


# Функция для отправки сообщения всем подключенным клиентам
async def broadcast_message(message: str):
    for connection in active_connections:
        await connection.send_text(message)

