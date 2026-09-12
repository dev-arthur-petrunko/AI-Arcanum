from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import Base, engine
from .models import System, Deck, Card, CardCorrespondence, Spread, SpreadPosition, QuizProgress  # noqa: F401 (register)
from .routers import systems, decks, cards, search, quiz, spreads, reference

app = FastAPI(title="Fortune-telling Cards API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"ok": True}


app.include_router(systems.router)
app.include_router(decks.router)
app.include_router(cards.router)
app.include_router(search.router)
app.include_router(quiz.router)
app.include_router(spreads.router)
app.include_router(reference.router)
