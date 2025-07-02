from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.auth.router import router as router_auth


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """
    Управление жизненным циклом приложения.
    """

    logger.info('Инициализация приложения...')
    yield
    logger.info('Завершение работы приложения...')


def create_app() -> FastAPI:
    """
   Создание и конфигурация FastAPI приложения.

   :return Сконфигурированное приложение FastAPI
   """

    app = FastAPI(
        title='Стартовая сборка FastAPI',
        description=(
            'Стартовая сборка с интегрированной SQLAlchemy 2 для разработки FastAPI приложений с продвинутой '
            'архитектурой, включающей авторизацию, аутентификацию и управление ролями пользователей.'
        ),
        version='1.0.0',
        lifespan=lifespan,
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    # Монтирование статических файлов
    app.mount(
        '/static',
        StaticFiles(directory='app/static'),
        name='static'
    )

    # Регистрация роутеров
    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Регистрация роутеров приложения."""
    # Корневой роутер
    root_router = APIRouter()

    @root_router.get('/', tags=['root'])
    def home_page():
        return {
            'message': 'Добро пожаловать!'
        }

    # Подключение роутеров
    app.include_router(root_router, tags=['root'])
    app.include_router(router_auth, prefix='/auth', tags=['Authentication'])


# Создание экземпляра приложения
app = create_app()
