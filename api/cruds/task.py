from sqlalchemy.orm import Session

import api.models.task as task_model
import api.schemas.task as task_schema


def create_task(db: Session, task_create: task_schema.TaskCreate) -> task_model.Task:  # task_schema.TaskCreate를 인수로 받음
    task = task_model.Task(**task_create.dict())  # db 모델인 task_model.Task로 변환
    db.add(task)
    db.commit()  # db commit
    db.refresh(task)  # Update task (Task instance)
    return task