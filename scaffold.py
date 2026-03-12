import os

dirs = [
    'backend',
    'backend/models',
    'backend/routers',
    'backend/services',
    'backend/data',
    'backend/ml',
    'backend/ml/models',
    'frontend',
    'frontend/app',
    'frontend/app/case',
    'frontend/app/case/[cnr]',
    'frontend/components',
    'frontend/lib',
    'scripts'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

empty_files_backend = [
    ('backend/main.py', 'from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\n'),
    ('backend/config.py', 'from pydantic_settings import BaseSettings\n'),
    ('backend/database.py', 'from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession\nfrom sqlalchemy.orm import declarative_base, sessionmaker\n'),
    ('backend/models/__init__.py', ''),
    ('backend/models/case.py', 'from sqlalchemy import Column, Integer, String\nfrom backend.database import Base\n'),
    ('backend/models/prediction.py', 'from sqlalchemy import Column, Integer, Float\nfrom backend.database import Base\n'),
    ('backend/routers/__init__.py', ''),
    ('backend/routers/cases.py', 'from fastapi import APIRouter\n'),
    ('backend/routers/predict.py', 'from fastapi import APIRouter\n'),
    ('backend/routers/precedents.py', 'from fastapi import APIRouter\n'),
    ('backend/routers/pathway.py', 'from fastapi import APIRouter\n'),
    ('backend/routers/report.py', 'from fastapi import APIRouter\n'),
    ('backend/services/__init__.py', ''),
    ('backend/services/ecourts.py', 'import httpx\n'),
    ('backend/services/njdg.py', 'from bs4 import BeautifulSoup\n'),
    ('backend/services/indian_kanoon.py', 'import httpx\n'),
    ('backend/services/groq_service.py', 'from groq import Groq\n'),
    ('backend/services/pinecone_service.py', 'from pinecone import Pinecone\n'),
    ('backend/services/prediction_engine.py', 'import xgboost as xgb\n'),
    ('backend/services/pathway_router.py', 'import json\n'),
    ('backend/services/pdf_generator.py', 'from reportlab.pdfgen import canvas\n'),
    ('backend/data/district_stats.json', '{}'),
    ('backend/ml/train_outcome.py', 'import xgboost as xgb\nimport sklearn\n'),
    ('backend/ml/models/outcome_model.pkl', ''),
    ('scripts/download_njdg_data.py', 'import httpx\n'),
    ('scripts/compute_district_stats.py', 'import pandas as pd\nimport json\n'),
    ('scripts/seed_pinecone.py', 'from pinecone import Pinecone\nfrom sentence_transformers import SentenceTransformer\n')
]

for fp, content in empty_files_backend:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

empty_files_frontend = [
    ('frontend/app/page.tsx', "import React from 'react';\n\nexport default function Page() {\n  return <div></div>;\n}\n"),
    ('frontend/app/layout.tsx', "import '../globals.css';\nimport React from 'react';\n\nexport default function RootLayout({ children }: { children: React.ReactNode }) {\n  return <html lang=\"en\"><body>{children}</body></html>;\n}\n"),
    ('frontend/app/globals.css', "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n"),
    ('frontend/app/case/[cnr]/page.tsx', "import React from 'react';\n\nexport default function CasePage({ params }: { params: { cnr: string } }) {\n  return <div></div>;\n}\n"),
    ('frontend/components/IntroScreen.tsx', "import React from 'react';\nexport default function IntroScreen() { return <div></div>; }\n"),
    ('frontend/components/SearchPanel.tsx', "import React from 'react';\nexport default function SearchPanel() { return <div></div>; }\n"),
    ('frontend/components/LoadingAnalysis.tsx', "import React from 'react';\nexport default function LoadingAnalysis() { return <div></div>; }\n"),
    ('frontend/components/ResultsDashboard.tsx', "import React from 'react';\nexport default function ResultsDashboard() { return <div></div>; }\n"),
    ('frontend/components/OutcomeCard.tsx', "import React from 'react';\nexport default function OutcomeCard() { return <div></div>; }\n"),
    ('frontend/components/DurationCard.tsx', "import React from 'react';\nexport default function DurationCard() { return <div></div>; }\n"),
    ('frontend/components/PathwayCard.tsx', "import React from 'react';\nexport default function PathwayCard() { return <div></div>; }\n"),
    ('frontend/components/BottleneckMap.tsx', "import React from 'react';\nexport default function BottleneckMap() { return <div></div>; }\n"),
    ('frontend/components/PrecedentGrid.tsx', "import React from 'react';\nexport default function PrecedentGrid() { return <div></div>; }\n"),
    ('frontend/components/RAGCitationBox.tsx', "import React from 'react';\nexport default function RAGCitationBox() { return <div></div>; }\n"),
    ('frontend/components/CitizenReport.tsx', "import React from 'react';\nexport default function CitizenReport() { return <div></div>; }\n"),
    ('frontend/lib/api.ts', "import axios from 'axios';\n"),
    ('frontend/lib/types.ts', "export interface CaseData {}\n"),
    ('frontend/tailwind.config.ts', "import type { Config } from 'tailwindcss';\nconst config: Config = { content: ['./app/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx,mdx}'], theme: { extend: {} }, plugins: [], };\nexport default config;\n"),
    ('frontend/tsconfig.json', '{\n  "compilerOptions": {\n    "target": "es5",\n    "lib": ["dom", "dom.iterable", "esnext"],\n    "allowJs": true,\n    "skipLibCheck": true,\n    "strict": true,\n    "noEmit": true,\n    "esModuleInterop": true,\n    "module": "esnext",\n    "moduleResolution": "bundler",\n    "resolveJsonModule": true,\n    "isolatedModules": true,\n    "jsx": "preserve",\n    "incremental": true,\n    "plugins": [\n      {\n        "name": "next"\n      }\n    ],\n    "paths": {\n      "@/*": ["./*"]\n    }\n  },\n  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],\n  "exclude": ["node_modules"]\n}\n'),
    ('frontend/next-env.d.ts', '/// <reference types="next" />\n/// <reference types="next/image-types/global" />\n')
]

for fp, content in empty_files_frontend:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

with open('.env.example', 'w', encoding='utf-8') as f:
    f.write('''# Database
DATABASE_URL=postgresql+asyncpg://user:pass@db.supabase.co:5432/postgres
REDIS_URL=redis://default:pass@endpoint.upstash.io:6379

# AI / LLM
GROQ_API_KEY=
PINECONE_API_KEY=
PINECONE_INDEX_NAME=drishti-cases
HUGGINGFACE_TOKEN=

# Data APIs
INDIAN_KANOON_API_KEY=

# App
SECRET_KEY=
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,https://drishti.vercel.app
LOG_LEVEL=INFO

# Frontend (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000
''')

with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write('''version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
''')

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write('''fastapi==0.109.0
uvicorn==0.27.0
SQLAlchemy==2.0.25
asyncpg==0.29.0
greenlet==3.0.3
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.1
httpx==0.26.0
beautifulsoup4==4.12.3
playwright==1.41.0
redis==5.0.1
groq==0.4.2
pinecone-client==3.0.2
sentence-transformers==2.3.1
xgboost==2.0.3
scikit-learn==1.4.0
pandas==2.2.0
reportlab==4.0.9
''')

with open('frontend/package.json', 'w', encoding='utf-8') as f:
    f.write('''{
  "name": "drishti-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "^18",
    "react-dom": "^18",
    "framer-motion": "^11.0.3",
    "recharts": "^2.11.0",
    "axios": "^1.6.7",
    "@tanstack/react-query": "^5.18.1"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "postcss": "^8",
    "tailwindcss": "^3.3.0",
    "eslint": "^8",
    "eslint-config-next": "14.1.0"
  }
}
''')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write('# DRISHTI\\n\\nPredictive Justice & Case Resolution Engine.\\n')

print("Scaffolding complete.")
