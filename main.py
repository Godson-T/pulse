from fastapi import FastAPI,WebSocket,WebSocketDisconnect,WebSocketException
from fastapi.responses import HTMLResponse,FileResponse

app=FastAPI()

class connectionManager:
    def __init__(self):
        self.room:dict[str,list[WebSocket]]={}
        
    async def connect(self,websocket:WebSocket,room_id: str):
        await websocket.accept()
        if room_id in self.room:
            self.room[room_id].append(websocket)
        else:
            self.room[room_id]=[]
            self.room[room_id].append(websocket)
            
    
    def disconnect(self,websocket:WebSocket,room_id:str):
        self.room[room_id].remove(websocket)
        if self.room[room_id]==[]:
            self.room.pop(room_id)
        
        
    async def broadcast(self,message:str,room_id: str):
        for connection in self.room[room_id]:
            await connection.send_text(message)
    
manager=connectionManager()    

@app.get("/")
def show_main():
    return FileResponse("index.html")

@app.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket,client_id: int,room_id: str):
    await manager.connect(websocket,room_id)
    try:
        while True:
            data=await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says:{data}",room_id)
                
                
    except WebSocketDisconnect:
        manager.disconnect(websocket,room_id)
        if room_id in manager.room:
            await manager.broadcast(f"Client #{client_id} has left the chat",room_id)
        