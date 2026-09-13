from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from .core.database import Base, engine
from .models import Article, System, Deck, Card, CardCorrespondence, Spread, SpreadPosition, QuizProgress  # noqa: F401 (реєстрація моделей)
from .routers import systems, decks, cards, search, quiz, spreads, reference, articles

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
app.include_router(articles.router)


class SystemAdmin(ModelView, model=System):
    column_list = [System.id, System.name, System.category, System.approx_year]
    column_searchable_list = [System.name]


class DeckAdmin(ModelView, model=Deck):
    column_list = [Deck.id, Deck.name, Deck.system_id, Deck.card_count, Deck.year]
    column_searchable_list = [Deck.name]


class CardAdmin(ModelView, model=Card):
    column_list = [Card.id, Card.deck_id, Card.number, Card.name, Card.arcana_type]
    column_searchable_list = [Card.name]


class ArticleAdmin(ModelView, model=Article):
    column_list = [Article.id, Article.slug, Article.title, Article.system]
    column_searchable_list = [Article.title]


admin = Admin(app, engine)
admin.add_view(SystemAdmin)
admin.add_view(DeckAdmin)
admin.add_view(CardAdmin)
admin.add_view(ArticleAdmin)
