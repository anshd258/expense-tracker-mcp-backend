from typing import Optional, Dict, Any
from datetime import datetime
from app.core.database import get_database
from app.utils.objectid import convert_object_id, prepare_mongo_doc
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserInDB


class UserService:
    @property
    def collection(self):
        """Get users collection"""
        return get_database()["users"]
    
    async def create_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Create a new user with hashed password"""
        user_dict = {
            "email": user_data.email,
            "hashed_password": get_password_hash(user_data.password),
            "full_name": user_data.full_name,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(user_dict)
        created_user = self.collection.find_one({"_id": result.inserted_id})
        return convert_object_id(created_user)
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        user = self.collection.find_one({"email": email})
        return convert_object_id(user) if user else None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        from bson import ObjectId
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        return convert_object_id(user) if user else None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user by email and password"""
        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user["hashed_password"]):
            return None
        return user
    
    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user information"""
        from bson import ObjectId
        update_data = prepare_mongo_doc(update_data)
        
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_user_by_id(user_id)
        return None


user_service = UserService()
