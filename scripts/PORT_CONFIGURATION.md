# Port Configuration - Documentation.AI

## Decision: Standardize on Port 5002

**Date:** December 2024  
**Status:** ✅ Implemented

## Background

The project had inconsistent port configurations across different files:
- `.env.example`: PORT=5000
- `app.py`: Default 5002 (if no PORT env var)
- `simple_server.py`: Default 5000 (if no PORT env var)  
- `frontend/package.json`: Proxy to localhost:5001
- `docker-compose.yml`: Port mapping 5000:5000
- `README.md`: References to localhost:5000

## Decision Rationale

**Chosen Port: 5002**

### Why Port 5002?

1. **Current Backend Default**: The main application (`app.py`) already defaults to port 5002
2. **Avoids Common Conflicts**: 
   - Port 3000: React dev server default
   - Port 5000: Common Flask default (used by many tutorials and other projects)
   - Port 5001: Often used by other development services
3. **Production Considerations**: Port 5002 is less likely to conflict with other services
4. **Consistency**: Aligns with the existing backend implementation

### Alternative Considered

**Port 5001**: This was the proxy target in the frontend, but:
- Creates potential conflicts with other services
- Doesn't match the backend's existing default
- Less common, providing no significant advantage

## Implementation Changes

### Files Updated:
1. ✅ `.env.example` - Updated PORT from 5000 to 5002
2. ✅ `frontend/package.json` - Updated proxy from localhost:5001 to localhost:5002
3. ✅ `docker-compose.yml` - Updated port mapping from 5000:5000 to 5002:5002  
4. ✅ `simple_server.py` - Updated default port from 5000 to 5002
5. ✅ `README.md` - Updated all references from localhost:5000 to localhost:5002

### Files Already Correct:
- `app.py` - Already uses port 5002 as default ✅

## Port Mapping Summary

| Service | Port | Purpose |
|---------|------|---------|
| Backend (Flask) | 5002 | Main API server |
| Frontend (React Dev) | 3000 | Development server |
| Frontend (Production) | 5002 | Served by Flask backend |
| Database (PostgreSQL) | 5432 | Database service |
| Redis | 6379 | Caching service |

## Usage

### Development Mode
```bash
# Backend runs on port 5002
python app.py

# Frontend dev server runs on port 3000, proxies API calls to 5002
cd frontend && npm start
```

### Production Mode
```bash
# Backend serves both API and built frontend on port 5002
python app.py
```

### Docker
```bash
# Backend accessible on port 5002
docker-compose up
```

## Environment Variables

Make sure your `.env` file contains:
```env
HOST=0.0.0.0
PORT=5002
```

## Benefits of This Configuration

1. **Consistent**: All components now use port 5002 for backend
2. **Conflict-Free**: Avoids common port conflicts with other dev tools
3. **Clear Separation**: Frontend dev (3000) vs Backend (5002) vs Production (5002)
4. **Docker Ready**: Port mapping is consistent across all deployment methods
5. **Future-Proof**: Less likely to conflict with new services

## Notes for Developers

- Always use `localhost:5002` when testing backend API directly
- Frontend proxy handles API calls automatically in development
- Production deployment serves everything from port 5002
- Update any local bookmarks or scripts to use port 5002

---

**This decision is now the standard for all Documentation.AI development and deployment.**
