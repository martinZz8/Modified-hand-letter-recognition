from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
import datetime
from models import BaseModel


class Prediction(BaseModel):
    _tablename__ = "prediction"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_id: Mapped[int]
    image_current_fullname: Mapped[str] = mapped_column(String(100))
    image_original_fullname: Mapped[str] = mapped_column(String(100))
    predicted_class: Mapped[str] = mapped_column(String(50))
    predicted_successful: Mapped[bool] = mapped_column(unique=False, default=False)
    evaluation_datetime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
