from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskListResponse
from app.services.task_service import (
    create_task,
    get_task,
    get_tasks,
    update_task,
    delete_task
)
from app.services.auth_service import get_current_user
from app.models.user import User

# api de tareas (prefijo de la llamada)
router = APIRouter(prefix="/tasks", tags=["tasks"])

# sufijo de la llamada
@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
# Crear una nueva tarea
def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
   # Crear una nueva tarea
    return create_task(db=db, task=task)

# Listar tareas con paginación
@router.get("/", response_model=TaskListResponse)
def list_tasks(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Obtener la lista de tareas con paginación
    return get_tasks(db=db, page=page, page_size=page_size)

# Obtener una tarea por ID
@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
   # valor de la tarea
    db_task = get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    return db_task

# Actualizar una tarea existente
@router.put("/{task_id}", response_model=Task)
def update_existing_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    db_task = update_task(db=db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    return db_task

# Eliminar una tarea
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    success = delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    return None