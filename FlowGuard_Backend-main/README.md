┌─────────────────────────────────────────┐
│              APP                        │
│   React / Next.js (frontend)            │
│   - Upload image                        │
│   - See detection results               │
│   - View inspection reports             │
└──────────────┬──────────────────────────┘
               │ HTTP requests (JSON)
               ▼
┌─────────────────────────────────────────┐
│           FastAPI (backend)             │
│   - Receive image                       │
│   - Call AI logic                       │
│   - Return results as JSON              │
└──────────────┬──────────────────────────┘
               │ Python function calls
               ▼
┌─────────────────────────────────────────┐
│           Core AI (Python)              │
│   - YOLOv8 detection                    │
│   - Geometric validation                │
│   - Topology validation                 │
│   - Decision engine                     │
└─────────────────────────────────────────┘


Core = The AI brain. Pure Python, no web stuff.
API = The waiter. Takes requests from frontend, gives them to the AI, returns the answer.
Frontend = The face. What the user actually sees and clicks.