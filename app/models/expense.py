from typing import Optional, Dict, Any, List
from datetime import datetime
from bson import ObjectId
from app.core.database import get_database
from app.utils.objectid import convert_object_id, prepare_mongo_doc
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseType


class ExpenseService:
    @property
    def collection(self):
        """Get expenses collection"""
        return get_database()["expenses"]
    
    async def create_expense(self, user_id: str, expense_data: ExpenseCreate) -> Dict[str, Any]:
        """Create a new expense"""
        expense_dict = {
            "user_id": user_id,
            "amount": expense_data.amount,
            "category": expense_data.category.value,
            "description": expense_data.description,
            "date": expense_data.date,
            "created_at": datetime.utcnow(),
            "updated_at": None
        }
        
        result = self.collection.insert_one(expense_dict)
        created_expense = self.collection.find_one({"_id": result.inserted_id})
        return convert_object_id(created_expense)
    
    async def get_expense_by_id(self, expense_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get expense by ID for a specific user"""
        expense = self.collection.find_one({
            "_id": ObjectId(expense_id),
            "user_id": user_id
        })
        return convert_object_id(expense) if expense else None
    
    async def get_user_expenses(
        self, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[ExpenseType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get all expenses for a user with optional filters"""
        query = {"user_id": user_id}
        
        if category:
            query["category"] = category.value
        
        if start_date or end_date:
            date_filter = {}
            if start_date:
                date_filter["$gte"] = start_date
            if end_date:
                date_filter["$lte"] = end_date
            query["date"] = date_filter
        
        expenses = self.collection.find(query).sort("date", -1).skip(skip).limit(limit)
        return [convert_object_id(expense) for expense in expenses]
    
    async def update_expense(
        self, 
        expense_id: str, 
        user_id: str, 
        update_data: ExpenseUpdate
    ) -> Optional[Dict[str, Any]]:
        """Update an expense"""
        update_dict = update_data.model_dump(exclude_none=True)
        if update_dict:
            update_dict["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(expense_id), "user_id": user_id},
                {"$set": update_dict}
            )
            
            if result.modified_count:
                return await self.get_expense_by_id(expense_id, user_id)
        return None
    
    async def delete_expense(self, expense_id: str, user_id: str) -> bool:
        """Delete an expense"""
        result = self.collection.delete_one({
            "_id": ObjectId(expense_id),
            "user_id": user_id
        })
        return result.deleted_count > 0
    
    async def get_expense_count(self, user_id: str) -> int:
        """Get total count of expenses for a user"""
        return self.collection.count_documents({"user_id": user_id})
    
    async def get_total_amount(self, user_id: str) -> float:
        """Get total amount spent by a user"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]["total"] if result else 0.0


expense_service = ExpenseService()
    
