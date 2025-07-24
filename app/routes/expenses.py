from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from datetime import datetime
from app.core.auth import get_current_user
from app.schemas.expense import (
    ExpenseCreate, ExpenseUpdate, ExpenseResponse, 
    ExpenseList, ExpenseType
)
from app.models.expense import expense_service
from app.utils.exceptions import BadRequestException, NotFoundException
from bson import ObjectId

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new expense"""
    created_expense = await expense_service.create_expense(
        user_id=current_user["id"],
        expense_data=expense_data
    )
    return ExpenseResponse(**created_expense)


@router.get("/", response_model=ExpenseList)
async def get_expenses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    category: Optional[ExpenseType] = Query(None, description="Filter by category"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user's expenses with optional filters"""
    expenses = await expense_service.get_user_expenses(
        user_id=current_user["id"],
        skip=skip,
        limit=limit,
        category=category,
        start_date=start_date,
        end_date=end_date
    )
    
    total = await expense_service.get_expense_count(current_user["id"])
    
    return ExpenseList(
        expenses=[ExpenseResponse(**expense) for expense in expenses],
        total=total
    )


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific expense by ID"""
    if not ObjectId.is_valid(expense_id):
        raise BadRequestException("Invalid expense ID format")
    
    expense = await expense_service.get_expense_by_id(
        expense_id=expense_id,
        user_id=current_user["id"]
    )
    
    if not expense:
        raise NotFoundException("Expense")
    
    return ExpenseResponse(**expense)


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str,
    expense_update: ExpenseUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update an expense"""
    if not ObjectId.is_valid(expense_id):
        raise BadRequestException("Invalid expense ID format")
    
    updated_expense = await expense_service.update_expense(
        expense_id=expense_id,
        user_id=current_user["id"],
        update_data=expense_update
    )
    
    if not updated_expense:
        raise NotFoundException("Expense")
    
    return ExpenseResponse(**updated_expense)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete an expense"""
    if not ObjectId.is_valid(expense_id):
        raise BadRequestException("Invalid expense ID format")
    
    deleted = await expense_service.delete_expense(
        expense_id=expense_id,
        user_id=current_user["id"]
    )
    
    if not deleted:
        raise NotFoundException("Expense")
    
    return None


@router.get("/stats/summary")
async def get_expense_summary(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get expense summary statistics"""
    total_amount = await expense_service.get_total_amount(current_user["id"])
    total_count = await expense_service.get_expense_count(current_user["id"])
    
    # Get category breakdown
    pipeline = [
        {"$match": {"user_id": current_user["id"]}},
        {"$group": {
            "_id": "$category",
            "total": {"$sum": "$amount"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"total": -1}}
    ]
    
    category_stats = list(expense_service.collection.aggregate(pipeline))
    
    return {
        "total_amount": total_amount,
        "total_expenses": total_count,
        "average_expense": total_amount / total_count if total_count > 0 else 0,
        "categories": {
            stat["_id"]: {
                "total": stat["total"],
                "count": stat["count"],
                "percentage": (stat["total"] / total_amount * 100) if total_amount > 0 else 0
            }
            for stat in category_stats
        }
    }