from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logger import log_database_query

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=settings.MAX_WORKERS * 2,
    max_overflow=10,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> Generator[AsyncSession, None, None]:
    """
    Get database session
    """
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        log_database_query(
            "Session rollback",
            context={"error": str(e)}
        )
        raise
    finally:
        await session.close()

class DatabaseSessionManager:
    """
    Database session manager for handling transactions
    """
    def __init__(self):
        self.session = None

    async def __aenter__(self) -> AsyncSession:
        self.session = SessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
            log_database_query(
                "Transaction rollback",
                context={
                    "error_type": exc_type.__name__,
                    "error": str(exc_val)
                }
            )
        else:
            await self.session.commit()
        await self.session.close()

async def create_tables():
    """
    Create all database tables
    """
    from app.db.base import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    """
    Drop all database tables
    """
    from app.db.base import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

class QueryTracker:
    """
    Track and log database queries
    """
    def __init__(self):
        self.queries = []

    def record_query(self, query: str, params: dict = None):
        self.queries.append({
            "query": query,
            "parameters": params
        })

    def clear(self):
        self.queries = []

    def get_queries(self):
        return self.queries

query_tracker = QueryTracker()

def track_queries(func):
    """
    Decorator to track database queries
    """
    from functools import wraps
    import time

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        query_tracker.clear()
        
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            
            for query in query_tracker.get_queries():
                log_database_query(
                    query["query"],
                    query["parameters"],
                    duration
                )
            
            return result
        except Exception as e:
            log_database_query(
                "Query execution failed",
                context={"error": str(e)}
            )
            raise
        finally:
            query_tracker.clear()
    
    return wrapper

class AsyncDatabaseConnection:
    """
    Async database connection context manager
    """
    def __init__(self):
        self.connection = None

    async def __aenter__(self):
        self.connection = await engine.connect()
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            await self.connection.close()

class TransactionContext:
    """
    Transaction context manager
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()

def get_transaction_context(session: AsyncSession) -> TransactionContext:
    """
    Get transaction context
    """
    return TransactionContext(session) 