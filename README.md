# Pulse

A real-time messaging service built with **FastAPI, WebSockets, JavaScript, and HTML**.

## Overview

Pulse is a real-time messaging application that allows users to communicate with other users in the same room without refreshing the webpage.

It uses WebSockets to establish persistent, bidirectional communication between the client and server. Users can create rooms, join existing active rooms, and exchange messages in real time.

The current implementation uses an in-memory connection manager to organize WebSocket connections by room.

## Features

- **Active Rooms:** View the rooms that currently have active connections.
- **Create Rooms:** Enter a room name to create a new room if it does not already exist.
- **Join Existing Rooms:** Join an existing room by entering its name.
- **Room-Based Broadcasting:** Send messages to all connected clients in the same room.
- **Room Isolation:** Messages are delivered only to clients connected to the corresponding room.
- **Automatic Room Cleanup:** Empty rooms are automatically removed when their last connected client disconnects.
- **Dynamic Chat Interface:** The active rooms section automatically hides after successfully joining a room.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | Backend framework |
| WebSockets | Real-time, bidirectional communication |
| JavaScript | Frontend interaction and WebSocket client |
| HTML | Webpage structure |

## How It Works

Pulse uses a room-based connection management system to organize connected clients.

### Connection Workflow

1. A user opens the Pulse application.
2. The frontend requests the currently active rooms from the `/get_rooms` endpoint.
3. The user enters a room name.
4. The browser establishes a WebSocket connection using the room ID and client ID.
5. The FastAPI server accepts the connection and registers the client in the corresponding room.
6. If the room does not exist, the server creates it.
7. When a client sends a message, the server broadcasts it to all connected clients in that room.
8. When a client disconnects, its WebSocket connection is removed from the room.
9. If the room has no remaining connections, the server removes the room.

### Room Management

The connection manager maintains active WebSocket connections using a Python dictionary.

Conceptual representation:

```python
rooms = {
    "room-A": [websocket_1, websocket_2],
    "room-B": [websocket_3]
}
```

Each room ID maps to a list of connected WebSocket clients.

This allows the server to broadcast messages to a specific room instead of broadcasting them to every connected client.

**Note:** Room information is currently stored in server memory. It is temporary and is lost when the server process stops or restarts.

## Getting Started

Follow these steps to run Pulse locally.

### 1. Clone the repository

```bash
git clone https://github.com/Godson-T/pulse.git
```

### 2. Navigate to the project directory

```bash
cd pulse
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn
```

### 5. Start the development server

```bash
uvicorn main:app --reload
```

### 6. Open Pulse

Visit:

```text
http://127.0.0.1:8000/
```

Open multiple browser tabs to test communication between different clients and rooms.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the chat interface |
| GET | `/get_rooms` | Returns the currently active room names |
| WebSocket | `/ws/{room_id}/{client_id}` | Establishes a WebSocket connection for a client in a specific room |

### WebSocket Example

```text
ws://127.0.0.1:8000/ws/room-A/12345
```

Here:

- `room-A` identifies the room.
- `12345` identifies the client in the current implementation.

The client ID is currently a temporary identifier, not an authenticated user identity.

## Testing

The current implementation was manually tested using three browser tabs.

### Test Setup

| Browser Tab | Room |
|---|---|
| Tab 1 | Room A |
| Tab 2 | Room A |
| Tab 3 | Room B |

### Test Results

| Test Case | Expected Result | Status |
|---|---|---|
| Two clients join Room A | Both clients connect successfully | Passed |
| Client in Room A sends a message | Other Room A clients receive it | Passed |
| Client in Room A sends a message | Room B clients do not receive it | Passed |
| One Room A client disconnects | Only that client's connection is removed | Passed |
| Last client leaves a room | Empty room is removed | Passed |
| Remaining Room A client sends a message | Messaging continues successfully | Passed |
| Room B remains connected | Room B is unaffected by Room A disconnections | Passed |

These tests verify room-based broadcasting, room isolation, and WebSocket connection cleanup.

## Current Limitations

- Room information is stored in memory and does not persist across server restarts.
- There is no user authentication yet.
- Client IDs are temporary and are not linked to registered user accounts.
- Message history is not stored in a database.
- The active room list refreshes when the page loads or the current user joins a room. It does not automatically refresh when another user joins or leaves.
- The current connection manager operates within a single server process.

## Roadmap

Pulse is being developed incrementally, with the following planned improvements.

### Phase 1 — Basic WebSocket Communication
- [x] Establish WebSocket connections.
- [x] Support multiple connected clients.
- [x] Implement connection management.
- [x] Handle client disconnections.

### Phase 2 — Room-Based Messaging
- [x] Implement room-based connection management.
- [x] Support room creation and joining.
- [x] Implement room-specific message broadcasting.
- [x] Add active room listing.
- [x] Automatically remove empty rooms.
- [x] Test room isolation using multiple clients.

### Phase 3 — Authentication
- [ ] Implement JWT-based WebSocket authentication.
- [ ] Associate authenticated users with connections.
- [ ] Display usernames instead of temporary client IDs.

### Phase 4 — Database Integration
- [ ] Integrate PostgreSQL and SQLAlchemy.
- [ ] Create user, room, and message models.
- [ ] Persist messages in the database.
- [ ] Load message history when users join rooms.

### Phase 5 — Notifications
- [ ] Track unread messages per user.
- [ ] Deliver missed messages when users come back online.
- [ ] Implement offline notification functionality.

### Phase 6 — Scalability
- [ ] Integrate Redis Pub/Sub.
- [ ] Support communication across multiple server instances.
- [ ] Document the multi-instance architecture.

### Phase 7 — Testing and Deployment
- [ ] Add automated tests for authentication and room management.
- [ ] Create a Dockerfile and Docker Compose configuration.
- [ ] Add an architecture diagram.
- [ ] Document installation, configuration, and deployment.

## Project Status

**Current Stage: Phase 2 — Room-Based Messaging Completed**

The next development milestone is JWT authentication for WebSocket connections.