import datetime
from decimal import Decimal

from sqlalchemy import Date, Integer, UniqueConstraint, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class StatisticalRecord(Base):
    __tablename__ = "statistical_records"
    __table_args__ = (UniqueConstraint("date", "respondent", name="date_respondent"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    respondent: Mapped[int] = mapped_column(Integer, nullable=False)
    sex: Mapped[int] = mapped_column(Integer, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[Decimal] = mapped_column(DECIMAL(26, 18), nullable=False)
