import os
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Animal Mixer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/mixer/config.js")
def mixer_config():
    return Response(
        content=(
            f'window.SUPABASE_URL="{os.getenv("SUPABASE_URL", "")}";'
            f'window.SUPABASE_ANON_KEY="{os.getenv("SUPABASE_ANON_KEY", "")}";'
        ),
        media_type="application/javascript",
    )


@app.get("/")
def root():
    return {"status": "ok", "app": "animal-mixer"}


# Static files — must come after explicit routes
app.mount("/mixer", StaticFiles(directory=".", html=True), name="mixer")
