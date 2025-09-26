# Teler VAPI Bridge

A reference integration between Teler and VAPI, based on Media Streaming over WebSockets.

## Setup

1. **Clone and configure:**

   ```bash
   git clone https://github.com/frejun-tech/teler-vapi-bridge.git
   cd teler-vapi-bridge
   cp env.example .env
   # Edit .env with your actual values
   ```

2. **Run with Docker:**
   ```bash
   docker compose up -d --build
   ```

## Environment Variables

| Variable                   | Description                     | Default  |
| -------------------------- | ------------------------------- | -------- |
| `VAPI_API_KEY`             | Your VAPI API key               | Required |
| `VAPI_ASSISTANT_ID`        | Your VAPI assistant ID          | Required |
| `VAPI_SAMPLE_RATE`         | Audio sample rate               | 16000    |
| `VAPI_MESSAGE_BUFFER_SIZE` | Messages to buffer before relay | 50       |
| `TELER_API_KEY`            | Your Teler API key              | Required |
| `NGROK_AUTHTOKEN`          | Your ngrok auth token           | Required |

## API Endpoints

- `GET /` - Health check with server domain
- `GET /health` - Service status
- `GET /ngrok-status` - Current ngrok status and URL
- `POST /api/v1/calls/initiate-call` - Start a new call with dynamic phone numbers
- `POST /api/v1/calls/flow` - Get call flow configuration
- `WebSocket /api/v1/calls/media-stream` - Audio streaming
- `POST /api/v1/webhooks/receiver` - Teler webhook receiver

### Call Initiation Example

```bash
curl -X POST "http://localhost:8000/api/v1/calls/initiate-call" \
  -H "Content-Type: application/json" \
  -d '{
    "from_number": "+1234567890",
    "to_number": "+0987654321"
  }'
```

## Features

- **Bi-directional media streaming** - Bridges audio between Teler and VAPI (Voice API) over WebSockets.
- **Real-time audio handling** - Receives live audio chunks from Teler, processes them, and forwards to VAPI; streams responses back to Teler.
- **Dockerized setup** - Comes with Dockerfile and docker-compose.yml for easy local development and deployment.
- **Dynamic ngrok URL detection** - Automatically detects current ngrok domain
- **Audio buffering** - Buffers VAPI messages before relaying to Teler
- **Sample rate conversion** - Converts VAPI 16kHz audio to Teler 8kHz
