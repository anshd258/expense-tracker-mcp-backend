from fastapi import APIRouter, Depends, Query, Response
from datetime import datetime
from io import StringIO
import csv
from app.core.auth import get_current_user
from app.core.database import get_database
from app.schemas.expense import DailyReport, WeeklyReport, MonthlyReport
from app.services.reports import get_daily_report, get_weekly_report, get_monthly_report

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/daily", response_model=DailyReport)
def daily_report(
    date: datetime = Query(default_factory=datetime.utcnow),
    current_user=Depends(get_current_user)
):
    report = get_daily_report(current_user["id"], date)
    return DailyReport(**report)

@router.get("/weekly", response_model=WeeklyReport)
def weekly_report(
    date: datetime = Query(default_factory=datetime.utcnow),
    current_user=Depends(get_current_user)
):
    report = get_weekly_report(current_user["id"], date)
    return WeeklyReport(**report)

@router.get("/monthly", response_model=MonthlyReport)
def monthly_report(
    year: int = Query(default_factory=lambda: datetime.utcnow().year),
    month: int = Query(default_factory=lambda: datetime.utcnow().month, ge=1, le=12),
    current_user=Depends(get_current_user)
):
    report = get_monthly_report(current_user["id"], year, month)
    return MonthlyReport(**report)

@router.get("/export/csv")
def export_csv(
    start_date: datetime = None,
    end_date: datetime = None,
    current_user=Depends(get_current_user)
):
    db = get_database()
    
    # Convert user_id to ObjectId for query
    from bson import ObjectId
    user_id = current_user["id"]
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    query = {"user_id": user_id}
    
    if start_date or end_date:
        date_query = {}
        if start_date:
            date_query["$gte"] = start_date
        if end_date:
            date_query["$lte"] = end_date
        query["date"] = date_query
    
    expenses = list(db.expenses.find(query).sort("created_at", -1))
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "Date", "Amount", "Category", "Description"
    ])
    
    for expense in expenses:
        writer.writerow([
            expense["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
            expense["amount"],
            expense["category"],
            expense["description"],
        ])
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=expenses_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        }
    )