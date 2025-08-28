# Teler VAPI Bridge

A FastAPI-based bridge service that connects Teler voice calls with VAPI AI assistants, enabling real-time voice conversations with AI.

## Features

- **Voice Call Integration**: Seamlessly bridge Teler voice calls with VAPI AI assistants
- **Real-time Audio Streaming**: Handle bidirectional audio streams between callers and AI
- **WebSocket Support**: Real-time communication for audio streaming
- **Webhook Handling**: Receive and process call status updates
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Public Access**: Use ngrok to expose your local API publicly

## Project Structure

```
teler-vapi-bridge/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py           # Main API router
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── calls.py        # Call-related endpoints
│   │       └── webhooks.py     # Webhook handling
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration management
│   └── utils/
│       ├── __init__.py
│       ├── stream_handlers.py  # Audio stream processing
│       ├── teler_client.py     # Teler API client
│       └── vapi_client.py      # VAPI API client
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variables template
└── README.md                   # This file
```

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- ngrok account and auth token
- Teler API key
- VAPI API key and assistant ID

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd teler-vapi-bridge
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your actual values:

```bash
# VAPI Configuration
VAPI_API_KEY=your_actual_vapi_api_key
VAPI_ASSISTANT_ID=your_actual_vapi_assistant_id
VAPI_SAMPLE_RATE=8000

# Server Configuration
SERVER_DOMAIN=your_ngrok_domain.ngrok.io
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Teler Configuration
TELER_API_KEY=your_actual_teler_api_key
FROM_NUMBER=+1234567890
TO_NUMBER=+0987654321

# Logging
LOG_LEVEL=INFO

# Ngrok Configuration
NGROK_AUTHTOKEN=your_actual_ngrok_auth_token
```

### 3. Run with Docker Compose

Start the application and ngrok:

```bash
docker-compose up -d
```

This will:
- Build and start the FastAPI application on port 8000
- Start ngrok to expose your local API publicly
- Make the ngrok dashboard available on port 4040

### 4. Get Your Public URL

Visit `http://localhost:4040` to see your ngrok dashboard and get your public URL.

Update your `.env` file with the ngrok domain:

```bash
SERVER_DOMAIN=abc123.ngrok.io
```

### 5. Restart the Application

After updating the SERVER_DOMAIN, restart the application:

```bash
docker-compose restart app
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint with service status
- `GET /health` - Health check endpoint

### Calls
- `GET /api/v1/calls/initiate-call` - Initiate a new call
- `POST /api/v1/calls/flow` - Get call flow configuration
- `WebSocket /api/v1/calls/media-stream` - Audio streaming endpoint

### Webhooks
- `POST /api/v1/webhooks/receiver` - Receive webhook callbacks from Teler

## Usage

### 1. Initiate a Call

```bash
curl -X GET "http://localhost:8000/api/v1/calls/initiate-call"
```

### 2. Monitor Webhooks

Webhooks from Teler will be automatically logged to the application logs.

### 3. View Logs

```bash
docker-compose logs -f app
```

## Development

### Local Development (without Docker)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables in `.env`

3. Run the application:
```bash
python -m app.main
```

### Running Tests

```bash
# Add test dependencies to requirements.txt
pytest
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VAPI_API_KEY` | Your VAPI API key | Required |
| `VAPI_ASSISTANT_ID` | Your VAPI assistant ID | Required |
| `VAPI_SAMPLE_RATE` | Audio sample rate | 8000 |
| `SERVER_DOMAIN` | Your public domain (ngrok) | Required |
| `TELER_API_KEY` | Your Teler API key | Required |
| `FROM_NUMBER` | Phone number to call from | +91123******* |
| `TO_NUMBER` | Phone number to call to | +91456******* |
| `LOG_LEVEL` | Logging level | INFO |
| `NGROK_AUTHTOKEN` | Your ngrok auth token | Required |

## Troubleshooting

### Common Issues

1. **ngrok not working**: Ensure your auth token is correct and ngrok is running
2. **Audio streaming issues**: Check that SERVER_DOMAIN is correctly set to your ngrok domain
3. **API key errors**: Verify your VAPI and Teler API keys are correct
4. **Port conflicts**: Ensure ports 8000 and 4040 are available

### Logs

Check application logs:
```bash
docker-compose logs app
```

Check ngrok logs:
```bash
docker-compose logs ngrok
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the repository
- Check the logs for error details
- Verify your configuration settings
