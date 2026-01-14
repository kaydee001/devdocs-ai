# DevDocs AI

AI-powered code documentation generator with quality scoring.

## Features

- 🔍 Code Analysis: AST-based parsing
- 📝 Doc Generation: LLM-powered README creation
- ⭐ Quality Scoring: 0-100 score with suggestions
- 📁 File Upload: Support for .py files
- 🎯 REST API: FastAPI with interactive docs

## Tech Stack

- FastAPI
- Groq API (Llama 3.3)
- Python AST
- Pydantic


## API Endpoints

- `POST /analyze` - Analyze code from JSON
- `POST /analyze/file` - Analyze .py file upload
- `GET /docs` - Interactive API documentation

## Status

✅ Core features complete  
⏳ Deployment in progress  
⏳ Docker containerization planned

## License

MIT