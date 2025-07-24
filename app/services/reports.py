from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from bson import ObjectId
from app.core.database import get_database

def get_daily_report(user_id: str, date: datetime) -> Dict:
    """
    Get expense summary for a single day.
    
    MongoDB Pipeline:
    1. $match: Filter expenses by user and date
    2. $group: Group by category and calculate totals
    """
    db = get_database()
    
    # Ensure user_id is ObjectId
    
    # Set date boundaries for the day (inclusive start, exclusive end)
    start_date = datetime(date.year, date.month, date.day)
    end_date = start_date + timedelta(days=1)
    
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "date": {"$gte": start_date, "$lt": end_date}
            }
        },
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1}
            }
        }
    ]
    print("Pipeline:", pipeline)
    results = list(db.expenses.aggregate(pipeline))
    print("Raw aggregation results:", results)
    categories = {result["_id"]: result["total"] for result in results}
    total_amount = sum(result["total"] for result in results)
    expenses_count = sum(result["count"] for result in results)
    final_result = {
        "date": start_date.strftime("%Y-%m-%d"),
        "total_amount": total_amount,
        "expenses_count": expenses_count,
        "categories": categories
    }
    print("Final return value:", final_result)
    return final_result


def get_weekly_report(user_id: str, date: datetime) -> Dict:
    """
    Get expense summary for a week with daily breakdown.
    """
    db = get_database()

    # Calculate week boundaries (Monday to Sunday)
    start_of_week = date - timedelta(days=date.weekday())
    start_of_week = datetime(start_of_week.year, start_of_week.month, start_of_week.day)
    end_of_week = start_of_week + timedelta(days=7)
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "date": {"$gte": start_of_week, "$lt": end_of_week}
            }
        },
        {
            "$group": {
                "_id": {
                    "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
                    "category": "$category"
                },
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1}
            }
        }
    ]
    results = list(db.expenses.aggregate(pipeline))
    daily_data = defaultdict(lambda: {"total_amount": 0, "expenses_count": 0, "categories": {}})
    overall_categories = defaultdict(float)
    for result in results:
        date_str = result["_id"]["date"]
        category = result["_id"]["category"]
        amount = result["total"]
        count = result["count"]
        daily_data[date_str]["total_amount"] += amount
        daily_data[date_str]["expenses_count"] += count
        daily_data[date_str]["categories"][category] = amount
        overall_categories[category] += amount
    daily_breakdown = []
    for i in range(7):
        current_date = start_of_week + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        if date_str in daily_data:
            daily_breakdown.append({
                "date": date_str,
                **daily_data[date_str]
            })
        else:
            daily_breakdown.append({
                "date": date_str,
                "total_amount": 0,
                "expenses_count": 0,
                "categories": {}
            })
    total_amount = sum(data["total_amount"] for data in daily_breakdown)
    expenses_count = sum(data["expenses_count"] for data in daily_breakdown)
    return {
        "week_start": start_of_week.strftime("%Y-%m-%d"),
        "week_end": (end_of_week - timedelta(days=1)).strftime("%Y-%m-%d"),
        "total_amount": total_amount,
        "expenses_count": expenses_count,
        "daily_breakdown": daily_breakdown,
        "categories": dict(overall_categories)
    }


def get_monthly_report(user_id: str, year: int, month: int) -> Dict:
    """
    Get expense summary for a month.
    """
    db = get_database()

    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "date": {"$gte": start_date, "$lt": end_date}
            }
        },
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1}
            }
        }
    ]
    results = list(db.expenses.aggregate(pipeline))
    categories = {result["_id"]: result["total"] for result in results}
    total_amount = sum(result["total"] for result in results)
    expenses_count = sum(result["count"] for result in results)
    days_in_month = (end_date - start_date).days
    daily_average = total_amount / days_in_month if days_in_month > 0 else 0
    return {
        "month": start_date.strftime("%B"),
        "year": year,
        "total_amount": total_amount,
        "expenses_count": expenses_count,
        "categories": categories,
        "daily_average": daily_average
    }


# Helper function to simplify date range queries
def get_expenses_summary(user_id: str, start_date: datetime, end_date: datetime) -> Dict:
    """
    Generic helper function to get expense summary for any date range.
    This reduces code duplication across different report types.
    """
    db = get_database()
    
    # Ensure user_id is ObjectId

    
    # Single pipeline that can be reused
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "date": {"$gte": start_date, "$lt": end_date}
            }
        },
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1}
            }
        }
    ]
    
    results = list(db.expenses.aggregate(pipeline))
    
    categories = {result["_id"]: result["total"] for result in results}
    total_amount = sum(result["total"] for result in results)
    expenses_count = sum(result["count"] for result in results)
    
    return {
        "total_amount": total_amount,
        "expenses_count": expenses_count,
        "categories": categories
    }