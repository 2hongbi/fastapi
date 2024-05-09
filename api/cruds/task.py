from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.task as task_model
import api.schemas.task as task_schema


def create_task(db: Session, task_create: task_schema.TaskCreate) -> task_model.Task:  # task_schema.TaskCreate를 인수로 받음
    task = task_model.Task(**task_create.dict())  # db 모델인 task_model.Task로 변환
    db.add(task)
    db.commit()  # db commit
    db.refresh(task)  # Update task (Task instance)
    return task


def get_tasks_with_done(db: Session) -> list[tuple[int, str, bool]]:
    result: Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Done.id.isnot(None).label("done"),  # Done.id가 존재하면 done=True, 존재하지 않으면 done=False
        ).outerjoin(task_model.Done)
    )

    return result.all()


def get_task(db: Session, task_id: int) -> task_model.Task | None:
    result: Result = db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )

    return result.scalars().first()


def update_task(db: Session, task_create: task_schema.TaskCreate, original:task_model.Task) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    db.commit()
    db.refresh(original)
    return original


def delete_task(db: Session, original: task_model.Task) -> None:
    db.delete(original)
    db.commit()