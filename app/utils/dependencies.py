from typing import Dict, Any, Optional
from fastapi import Query
from datetime import datetime


class PaginationParams:
    """Common pagination parameters"""
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(10, ge=1, le=100, description="Number of items to return")
    ):
        self.skip = skip
        self.limit = limit


class DateRangeParams:
    """Common date range filter parameters"""
    def __init__(
        self,
        start_date: Optional[datetime] = Query(None, description="Start date filter"),
        end_date: Optional[datetime] = Query(None, description="End date filter")
    ):
        self.start_date = start_date
        self.end_date = end_date
    
    def get_filter(self) -> Dict[str, Any]:
        """Get MongoDB date filter"""
        if not self.start_date and not self.end_date:
            return {}
        
        date_filter = {}
        if self.start_date:
            date_filter["$gte"] = self.start_date
        if self.end_date:
            date_filter["$lte"] = self.end_date
        
        return {"date": date_filter}