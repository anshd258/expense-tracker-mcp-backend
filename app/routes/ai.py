# from fastapi import APIRouter, Depends
# from app.core.auth import get_current_user
# from app.schemas.expense import ExpenseInsightsRequest, ExpenseInsightsResponse, SpendingAnalysisResponse
# from app.ml.gemini_analyzer import gemini_analyzer

# router = APIRouter(prefix="/ai", tags=["ai"])

# @router.post("/insights", response_model=ExpenseInsightsResponse)
# async def get_expense_insights(
#     request: ExpenseInsightsRequest,
#     current_user=Depends(get_current_user)
# ):
#     """
#     Generate AI-powered insights about user's expenses for a specified period.
#     Provides trends, patterns, and personalized recommendations.
#     """
#     insights_data = await gemini_analyzer.generate_insights(
#         user_id=str(current_user["_id"]),
#         period=request.period
#     )
    
#     return ExpenseInsightsResponse(**insights_data)

# @router.get("/analysis", response_model=SpendingAnalysisResponse)
# async def get_spending_analysis(
#     current_user=Depends(get_current_user)
# ):
#     """
#     Get comprehensive spending analysis including patterns, forecasts,
#     and detailed breakdowns of the last 3 months of expenses.
#     """
#     analysis_data = await gemini_analyzer.analyze_spending_patterns(
#         user_id=str(current_user["_id"])
#     )
    
#     return SpendingAnalysisResponse(**analysis_data)