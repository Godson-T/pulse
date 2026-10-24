from fastapi import FastAPI,WebSocket,WebSocketDisconnect,WebSocketException
from fastapi.responses import HTMLResponse,FileResponse

app=FastAPI()

class connectionManager:
    def __init__(self):
        self.active_connections:list[WebSocket]=[]
        
    async def connect(self,websocket:WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self,websocket=WebSocket):
        self.active_connections.remove(websocket)
        
    async def send_personal_messages(self,message: str,websocket:WebSocket):
        await websocket.send_text(message)
        
    async def broadcast(self,message:str):
        for connection in self.active_connections:
            await connection.send_text(message)
    
manager=connectionManager()    

@app.get("/")
def show_main():
    return FileResponse("index.html")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket,client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data=await websocket.receive_text()
            await manager.send_personal_messages(f"You wrote:{data}",websocket)
            await manager.broadcast(f"Client #{client_id} says:{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")
        