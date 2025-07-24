from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class ExpenseType(str, Enum):
    FOOD = "FOOD"
    TRANSPORT = "TRANSPORT"
    ENTERTAINMENT = "ENTERTAINMENT"
    UTILITIES = "UTILITIES"
    HEALTHCARE = "HEALTHCARE"
    SHOPPING = "SHOPPING"
    OTHER = "OTHER"


class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0, description="Expense amount must be positive")
    category: ExpenseType
    description: str = Field(..., min_length=1, max_length=500)
    date: datetime


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[ExpenseType] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    date: Optional[datetime] = None


class ExpenseResponse(ExpenseBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
    


class ExpenseList(BaseModel):
    expenses: List[ExpenseResponse]
    total: int

class DailyReport(BaseModel):
    date: str
    total_amount: float
    expenses_count: int
    categories: dict

class WeeklyReport(BaseModel):
    week_start: str
    week_end: str
    total_amount: float
    expenses_count: int
    daily_breakdown: List[DailyReport]
    categories: dict

class MonthlyReport(BaseModel):
    month: str
    year: int
    total_amount: float
    expenses_count: int
    categories: dict
    daily_average: float

class ExpenseInsightsRequest(BaseModel):
    period: str = "month"  # "week", "month", "quarter", "year"
    
class ExpenseInsightsResponse(BaseModel):
    insights: str
    trends: dict
    recommendations: List[str]
    
class SpendingAnalysisResponse(BaseModel):
    analysis: str
    category_breakdown: dict
    spending_patterns: dict
    forecast: dict