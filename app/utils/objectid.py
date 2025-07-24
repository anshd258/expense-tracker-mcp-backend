from typing import Any, Dict
from bson import ObjectId


def convert_object_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB _id to id for API responses"""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


def prepare_mongo_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare document for MongoDB insertion by removing id field"""
    if "id" in doc:
        del doc["id"]
    return doc