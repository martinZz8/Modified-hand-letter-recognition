from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, func
import datetime
from models.own_compiles.UtcDateTime import utcnow
from models.BaseModel import BaseModel


class Prediction(BaseModel):
    __tablename__ = "prediction"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_id: Mapped[str] = mapped_column(String(50))
    image_current_fullname: Mapped[str] = mapped_column(String(100))
    image_original_fullname: Mapped[str] = mapped_column(String(100))
    predicted_class: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    predicted_successful: Mapped[bool]
    # Timestamp based on: https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    # - for current timezone's datetime we use "server_default=func.now()"
    # - for UTC datetime we use "server_default=utcnow()"
    evaluation_datetime_utc: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), server_default=utcnow())
    execution_length_sec: Mapped[float] = mapped_column(Float(2), nullable=True)
    used_cuda: Mapped[bool]
