# CAMAS Setup & Deployment Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.11+
- Node.js 20+
- Ollama (optional, for local LLM serving)

### Development Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install frontend dependencies
cd frontend
npm install
cd ..

# 4. Configure environment
cp config/config.yaml config/config.yaml  # Adjust as needed

# 5. Start backend (in one terminal)
uvicorn app:app --reload --port 8000

# 6. Start frontend (in another terminal)
cd frontend
npm run dev  # Opens at http://localhost:5173
```

### Accessing the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Docker Deployment (Recommended for Competition)

### Build and Run with Docker Compose

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f camas

# Stop services
docker-compose down
```

The application will be available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000

---

## Configuration

Edit `config/config.yaml` to customize:

```yaml
ollama:
  base_url: "http://localhost:11434"  # Ollama endpoint
  models:
    simple: "phi3"
    medium: "llama3.2:3b"
    complex: "llama3.2:8b"

routing:
  complexity_thresholds:
    simple_max: 3.0      # < 3.0 → phi3
    medium_max: 7.0      # 3.0-7.0 → llama3.2:3b

energy:
  mock_mode: true        # Use mock measurements for demo

carbon:
  mock_mode: true
  mock_intensity_g_per_kwh: 400.0  # Global average

experiment:
  prompts_file: "experiments/prompts.json"
  database_path: "database/camas.db"
  results_dir: "reports"
  visualization_dir: "visualizations"
```

---

## Running Experiments

### Via Python CLI

```bash
# Run baseline experiment (50 queries)
python run_experiment.py --mode baseline --max-queries 50

# Run CAMAS experiment (50 queries)
python run_experiment.py --mode camas --max-queries 50

# Run both modes and generate reports
python run_experiment.py
```

### Via API

```bash
# Single query execution
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?", "mode": "camas"}'

# Start experiment
curl -X POST http://localhost:8000/experiment/run \
  -H "Content-Type: application/json" \
  -d '{"mode": "camas", "max_queries": 20}'

# Get experiment results
curl http://localhost:8000/experiment/{run_id}/summary

# Generate reports
curl -X POST http://localhost:8000/reports/generate
```

---

## Frontend Development

### Available Scripts

```bash
cd frontend

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

### Building Frontend Separately

```bash
cd frontend
npm run build
# Output: frontend/dist/
```

---

## Troubleshooting

### Ollama Connection Failed
If you see "Ollama not reachable", the system will automatically fall back to mock responses:
- Ensure Ollama is running: `ollama serve`
- Or set `energy.mock_mode: true` in config

### Database Errors
```bash
# Reset database
rm database/camas.db
# It will be recreated on first run
```

### Port Already in Use
```bash
# Change ports in config or use:
uvicorn app:app --port 8001  # Backend
cd frontend && npm run dev -- --port 5174  # Frontend
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
cd frontend && npm install --force && npm run build
```

---

## Production Deployment

### Using Gunicorn (Recommended)

```bash
pip install gunicorn
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker (Recommended)

```bash
# Build image
docker build -t camas:latest .

# Run container
docker run -d \
  --name camas \
  -p 8000:8000 \
  -v $(pwd)/database:/app/database \
  -v $(pwd)/reports:/app/reports \
  camas:latest
```

### Environment Variables (for production)

```bash
export VITE_API_URL=https://api.example.com
export CAMAS_OLLAMA_URL=http://ollama:11434
export CAMAS_DB_PATH=/data/camas.db
export PYTHONUNBUFFERED=1
```

---

## API Documentation

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| POST | `/query` | Execute single query |
| GET | `/experiments` | List all experiments |
| POST | `/experiment/run` | Start experiment |
| GET | `/experiment/{run_id}/summary` | Get results |
| POST | `/reports/generate` | Generate reports |

---

## Database Schema

CAMAS uses SQLite with these tables:

- `experiments` - Experiment runs and metadata
- `queries` - Individual query executions
- `energy_logs` - Energy measurements
- `carbon_logs` - Carbon predictions
- `routing_logs` - Routing decisions
- `sleep_logs` - Power management events
- `performance_logs` - Aggregated metrics
- `resource_logs` - Resource allocations

Access directly:
```bash
sqlite3 database/camas.db
sqlite> SELECT * FROM performance_logs LIMIT 10;
```

---

## Performance Tips

1. **Use mock mode for fast iteration** during development
2. **Run experiments in batches** (20-50 queries at a time)
3. **Cache experiment results** before regenerating reports
4. **Use indexes** for large datasets:
   ```sql
   CREATE INDEX idx_run_id ON performance_logs(run_id);
   ```

---

## Support & Documentation

- **GitHub:** https://github.com/Praveen4278/camas
- **Paper:** See `paper/` directory
- **Issues:** Report in GitHub Issues
- **Documentation:** Full API docs in app

---

## License

MIT License - See LICENSE file

---

**Last Updated:** November 2026
**Version:** 1.0.0
