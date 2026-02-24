"""
Metrics Helper Module
Provides convenient functions for recording Prometheus metrics throughout the application.
"""
import time
import functools
from contextlib import contextmanager
from typing import Callable, Optional, Any

from app.observability import (
    DB_QUERY_DURATION_SECONDS,
    DB_QUERY_TOTAL,
    AUTH_VALIDATION_TOTAL,
    TASK_OPERATIONS_TOTAL,
    GOAL_OPERATIONS_TOTAL,
    HABIT_OPERATIONS_TOTAL,
    TIMER_OPERATIONS_TOTAL,
    PROJECT_OPERATIONS_TOTAL,
    CACHE_OPERATIONS_TOTAL,
    CACHE_DURATION_SECONDS,
    EXTERNAL_SERVICE_REQUESTS_TOTAL,
    EXTERNAL_SERVICE_DURATION_SECONDS,
    ERRORS_TOTAL,
)


# ============= Database Metrics Helpers =============

@contextmanager
def track_db_query(operation: str, table: str):
    """
    Context manager to track database query metrics.

    Usage:
        with track_db_query("SELECT", "tasks"):
            result = db.session.query(Task).all()
    """
    start_time = time.perf_counter()
    status = "success"

    try:
        yield
    except Exception as e:
        status = "error"
        raise
    finally:
        duration = time.perf_counter() - start_time
        DB_QUERY_DURATION_SECONDS.labels(operation=operation, table=table).observe(duration)
        DB_QUERY_TOTAL.labels(operation=operation, table=table, status=status).inc()


def track_db_query_decorator(operation: str, table: str):
    """
    Decorator to track database query metrics.

    Usage:
        @track_db_query_decorator("SELECT", "tasks")
        def get_all_tasks():
            return db.session.query(Task).all()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with track_db_query(operation, table):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# ============= Auth Metrics Helpers =============

def record_auth_validation(validation_type: str, success: bool):
    """
    Record authentication validation attempt.

    Args:
        validation_type: Type of validation (jwt, session, oauth)
        success: Whether validation was successful
    """
    status = "success" if success else "failed"
    AUTH_VALIDATION_TOTAL.labels(validation_type=validation_type, status=status).inc()


# ============= Business Logic Metrics Helpers =============

def record_task_operation(operation: str, success: bool = True):
    """
    Record task operation.

    Args:
        operation: Operation type (create, update, delete, complete)
        success: Whether operation was successful
    """
    status = "success" if success else "failed"
    TASK_OPERATIONS_TOTAL.labels(operation=operation, status=status).inc()


def record_goal_operation(operation: str, success: bool = True):
    """
    Record goal operation.

    Args:
        operation: Operation type (create, update, delete, complete)
        success: Whether operation was successful
    """
    status = "success" if success else "failed"
    GOAL_OPERATIONS_TOTAL.labels(operation=operation, status=status).inc()


def record_habit_operation(operation: str, success: bool = True):
    """
    Record habit operation.

    Args:
        operation: Operation type (create, update, delete, track)
        success: Whether operation was successful
    """
    status = "success" if success else "failed"
    HABIT_OPERATIONS_TOTAL.labels(operation=operation, status=status).inc()


def record_timer_operation(operation: str, success: bool = True):
    """
    Record timer operation.

    Args:
        operation: Operation type (start, stop, complete)
        success: Whether operation was successful
    """
    status = "success" if success else "failed"
    TIMER_OPERATIONS_TOTAL.labels(operation=operation, status=status).inc()


def record_project_operation(operation: str, success: bool = True):
    """
    Record project operation.

    Args:
        operation: Operation type (create, update, delete)
        success: Whether operation was successful
    """
    status = "success" if success else "failed"
    PROJECT_OPERATIONS_TOTAL.labels(operation=operation, status=status).inc()


# ============= Cache Metrics Helpers =============

@contextmanager
def track_cache_operation(operation: str):
    """
    Context manager to track cache operation metrics.

    Usage:
        with track_cache_operation("get"):
            value = cache.get(key)
    """
    start_time = time.perf_counter()
    status = "hit"  # Default to hit, will be updated on miss

    try:
        yield
    except Exception:
        status = "error"
        raise
    finally:
        duration = time.perf_counter() - start_time
        CACHE_DURATION_SECONDS.labels(operation=operation).observe(duration)
        CACHE_OPERATIONS_TOTAL.labels(operation=operation, status=status).inc()


def record_cache_hit():
    """Record a cache hit."""
    CACHE_OPERATIONS_TOTAL.labels(operation="get", status="hit").inc()


def record_cache_miss():
    """Record a cache miss."""
    CACHE_OPERATIONS_TOTAL.labels(operation="get", status="miss").inc()


def record_cache_set():
    """Record a cache set operation."""
    CACHE_OPERATIONS_TOTAL.labels(operation="set", status="success").inc()


def record_cache_delete():
    """Record a cache delete operation."""
    CACHE_OPERATIONS_TOTAL.labels(operation="delete", status="success").inc()


# ============= External Service Metrics Helpers =============

@contextmanager
def track_external_service_call(service: str, operation: str):
    """
    Context manager to track external service call metrics.

    Usage:
        with track_external_service_call("auth-service", "validate_token"):
            response = auth_client.validate_token(token)
    """
    start_time = time.perf_counter()
    status = "success"

    try:
        yield
    except Exception:
        status = "error"
        raise
    finally:
        duration = time.perf_counter() - start_time
        EXTERNAL_SERVICE_DURATION_SECONDS.labels(service=service, operation=operation).observe(duration)
        EXTERNAL_SERVICE_REQUESTS_TOTAL.labels(service=service, operation=operation, status=status).inc()


# ============= Error Metrics Helpers =============

def record_error(error_type: str, component: str):
    """
    Record an application error.

    Args:
        error_type: Type of error (validation_error, database_error, etc.)
        component: Component where error occurred (api, repository, etc.)
    """
    ERRORS_TOTAL.labels(error_type=error_type, component=component).inc()


# ============= Generic Operation Tracker =============

def track_operation(metrics_counter, operation: str):
    """
    Generic decorator to track operations using any metric counter.

    Usage:
        @track_operation(TASK_OPERATIONS_TOTAL, "create")
        def create_task(data):
            # ... implementation
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                metrics_counter.labels(operation=operation, status="success").inc()
                return result
            except Exception:
                metrics_counter.labels(operation=operation, status="failed").inc()
                raise
        return wrapper
    return decorator
