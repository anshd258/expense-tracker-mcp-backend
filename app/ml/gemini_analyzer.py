# from google import genai
# from google.genai import types
# import asyncio
# from datetime import datetime, timedelta
# from typing import Dict, List
# from app.core.config import settings
# from app.core.database import get_database

# class GeminiExpenseAnalyzer:
#     def __init__(self):
#         self.client = genai.Client()
        
#     async def generate_insights(self, user_id: str, period: str = "month") -> Dict:
#         db = get_database()
        
#         # Calculate date range based on period
#         end_date = datetime.utcnow()
#         if period == "week":
#             start_date = end_date - timedelta(days=7)
#         elif period == "month":
#             start_date = end_date - timedelta(days=30)
#         elif period == "quarter":
#             start_date = end_date - timedelta(days=90)
#         elif period == "year":
#             start_date = end_date - timedelta(days=365)
#         else:
#             start_date = end_date - timedelta(days=30)
        
#         # Fetch user expenses
#         expenses = list(db.expenses.find({
#             "user_id": user_id,
#             "date": {"$gte": start_date, "$lte": end_date}
#         }).sort("date", -1))
        
#         if not expenses:
#             return {
#                 "insights": "No expenses found for the selected period.",
#                 "trends": {},
#                 "recommendations": ["Start tracking your expenses to get personalized insights!"]
#             }
        
#         # Prepare expense data for analysis
#         expense_summary = self._prepare_expense_summary(expenses)
        
#         prompt = f"""
#         Analyze the following expense data and provide valuable insights:
        
#         Period: {period}
#         Total Expenses: ${expense_summary['total_amount']:.2f}
#         Number of Transactions: {expense_summary['count']}
        
#         Category Breakdown:
#         {self._format_categories(expense_summary['categories'])}
        
#         Recent Transactions:
#         {self._format_recent_transactions(expenses[:10])}
        
#         Please provide:
#         1. Key insights about spending patterns
#         2. Trends observed in the data
#         3. Specific, actionable recommendations for better financial management
#         4. Any unusual spending patterns or concerns
        
#         Format the response as a detailed analysis that would be valuable to someone trying to manage their finances better.
#         """
        
#         try:
#             response = await asyncio.to_thread(
#                 self.client.models.generate_content,
#                 model="gemini-2.0-flash",
#                 contents=prompt,
#                 config=types.GenerateContentConfig(
#                     temperature=0.7,
#                     max_output_tokens=1000,
#                 )
#             )
            
#             # Extract insights from response
#             insights_text = response.text
            
#             # Calculate trends
#             trends = self._calculate_trends(expenses, expense_summary)
            
#             # Generate recommendations based on data
#             recommendations = await self._generate_recommendations(expense_summary, insights_text)
            
#             return {
#                 "insights": insights_text,
#                 "trends": trends,
#                 "recommendations": recommendations
#             }
            
#         except Exception as e:
#             print(f"Error generating insights: {e}")
#             return {
#                 "insights": "Unable to generate insights at this time.",
#                 "trends": {},
#                 "recommendations": []
#             }
    
#     async def analyze_spending_patterns(self, user_id: str) -> Dict:
#         db = get_database()
        
#         # Get last 3 months of data
#         end_date = datetime.utcnow()
#         start_date = end_date - timedelta(days=90)
        
#         expenses = list(db.expenses.find({
#             "user_id": user_id,
#             "date": {"$gte": start_date, "$lte": end_date}
#         }).sort("date", -1))
        
#         if not expenses:
#             return {
#                 "analysis": "No expense data available for analysis.",
#                 "category_breakdown": {},
#                 "spending_patterns": {},
#                 "forecast": {}
#             }
        
#         # Analyze by category
#         category_breakdown = self._analyze_by_category(expenses)
        
#         # Identify spending patterns
#         patterns = self._identify_patterns(expenses)
        
#         # Create forecast
#         forecast = self._create_forecast(expenses, category_breakdown)
        
#         prompt = f"""
#         Based on the following spending data from the last 3 months, provide a comprehensive analysis:
        
#         Total Spending: ${sum(e['amount'] for e in expenses):.2f}
#         Average Daily Spending: ${sum(e['amount'] for e in expenses) / 90:.2f}
        
#         Category Analysis:
#         {self._format_category_analysis(category_breakdown)}
        
#         Spending Patterns:
#         {self._format_patterns(patterns)}
        
#         Please provide:
#         1. Detailed analysis of spending habits
#         2. Areas of concern or opportunity
#         3. Comparison with typical spending patterns
#         4. Specific strategies for optimization
        
#         Be specific and actionable in your recommendations.
#         """
        
#         try:
#             response = await asyncio.to_thread(
#                 self.client.models.generate_content,
#                 model="gemini-2.0-flash",
#                 contents=prompt,
#                 config=types.GenerateContentConfig(
#                     temperature=0.7,
#                     max_output_tokens=1200,
#                 )
#             )
            
#             return {
#                 "analysis": response.text,
#                 "category_breakdown": category_breakdown,
#                 "spending_patterns": patterns,
#                 "forecast": forecast
#             }
            
#         except Exception as e:
#             print(f"Error analyzing spending patterns: {e}")
#             return {
#                 "analysis": "Unable to analyze spending patterns at this time.",
#                 "category_breakdown": category_breakdown,
#                 "spending_patterns": patterns,
#                 "forecast": forecast
#             }
    
#     def _prepare_expense_summary(self, expenses: List[Dict]) -> Dict:
#         summary = {
#             "total_amount": sum(e['amount'] for e in expenses),
#             "count": len(expenses),
#             "categories": {}
#         }
        
#         for expense in expenses:
#             category = expense['category']
#             if category not in summary['categories']:
#                 summary['categories'][category] = {"amount": 0, "count": 0}
#             summary['categories'][category]['amount'] += expense['amount']
#             summary['categories'][category]['count'] += 1
        
#         return summary
    
#     def _format_categories(self, categories: Dict) -> str:
#         lines = []
#         for cat, data in sorted(categories.items(), key=lambda x: x[1]['amount'], reverse=True):
#             percentage = (data['amount'] / sum(c['amount'] for c in categories.values())) * 100
#             lines.append(f"- {cat}: ${data['amount']:.2f} ({percentage:.1f}%) - {data['count']} transactions")
#         return "\n".join(lines)
    
#     def _format_recent_transactions(self, expenses: List[Dict]) -> str:
#         lines = []
#         for exp in expenses:
#             date_str = exp['date'].strftime("%Y-%m-%d")
#             lines.append(f"- {date_str}: {exp['description']} - ${exp['amount']:.2f} ({exp['category']})")
#         return "\n".join(lines)
    
#     def _calculate_trends(self, expenses: List[Dict], summary: Dict) -> Dict:
#         # Calculate weekly averages
#         weeks = {}
#         for expense in expenses:
#             week = expense['date'].strftime("%Y-%W")
#             if week not in weeks:
#                 weeks[week] = 0
#             weeks[week] += expense['amount']
        
#         # Determine trend direction
#         week_values = list(weeks.values())
#         if len(week_values) >= 2:
#             recent_avg = sum(week_values[-2:]) / 2
#             older_avg = sum(week_values[:-2]) / len(week_values[:-2]) if len(week_values) > 2 else week_values[0]
#             trend_direction = "increasing" if recent_avg > older_avg else "decreasing"
#             trend_percentage = abs((recent_avg - older_avg) / older_avg * 100)
#         else:
#             trend_direction = "stable"
#             trend_percentage = 0
        
#         return {
#             "direction": trend_direction,
#             "percentage": trend_percentage,
#             "weekly_average": sum(week_values) / len(week_values) if week_values else 0,
#             "highest_week": max(weeks.values()) if weeks else 0,
#             "lowest_week": min(weeks.values()) if weeks else 0
#         }
    
#     async def _generate_recommendations(self, summary: Dict, insights: str) -> List[str]:
#         recommendations = []
        
#         # High spending categories
#         for cat, data in summary['categories'].items():
#             percentage = (data['amount'] / summary['total_amount']) * 100
#             if percentage > 30:
#                 recommendations.append(f"Consider reducing {cat} expenses, which account for {percentage:.1f}% of your spending")
        
#         # Frequency-based recommendations
#         daily_avg = summary['total_amount'] / 30  # Assuming month period
#         if daily_avg > 100:
#             recommendations.append("Your daily spending average is high. Consider setting daily spending limits")
        
#         # Category-specific tips
#         if 'FOOD' in summary['categories'] and summary['categories']['FOOD']['count'] > 20:
#             recommendations.append("Frequent food expenses detected. Consider meal planning to reduce dining out")
        
#         if 'ENTERTAINMENT' in summary['categories']:
#             ent_percentage = (summary['categories']['ENTERTAINMENT']['amount'] / summary['total_amount']) * 100
#             if ent_percentage > 15:
#                 recommendations.append("Entertainment spending is above recommended 15%. Look for free or low-cost alternatives")
        
#         return recommendations[:5]  # Return top 5 recommendations
    
#     def _analyze_by_category(self, expenses: List[Dict]) -> Dict:
#         categories = {}
#         for expense in expenses:
#             cat = expense['category']
#             if cat not in categories:
#                 categories[cat] = {
#                     'total': 0,
#                     'count': 0,
#                     'average': 0,
#                     'max': 0,
#                     'min': float('inf')
#                 }
#             categories[cat]['total'] += expense['amount']
#             categories[cat]['count'] += 1
#             categories[cat]['max'] = max(categories[cat]['max'], expense['amount'])
#             categories[cat]['min'] = min(categories[cat]['min'], expense['amount'])
        
#         # Calculate averages
#         for cat in categories:
#             categories[cat]['average'] = categories[cat]['total'] / categories[cat]['count']
#             if categories[cat]['min'] == float('inf'):
#                 categories[cat]['min'] = 0
        
#         return categories
    
#     def _identify_patterns(self, expenses: List[Dict]) -> Dict:
#         patterns = {
#             'peak_spending_day': {},
#             'recurring_expenses': [],
#             'spending_velocity': 'normal'
#         }
        
#         # Day of week analysis
#         day_spending = {}
#         for expense in expenses:
#             day_name = expense['date'].strftime("%A")
#             if day_name not in day_spending:
#                 day_spending[day_name] = 0
#             day_spending[day_name] += expense['amount']
        
#         if day_spending:
#             peak_day = max(day_spending, key=day_spending.get)
#             patterns['peak_spending_day'] = {
#                 'day': peak_day,
#                 'amount': day_spending[peak_day]
#             }
        
#         # Identify recurring expenses (similar amounts)
#         amount_groups = {}
#         for expense in expenses:
#             rounded_amount = round(expense['amount'], 0)
#             if rounded_amount not in amount_groups:
#                 amount_groups[rounded_amount] = []
#             amount_groups[rounded_amount].append(expense)
        
#         for amount, group in amount_groups.items():
#             if len(group) >= 3:  # At least 3 occurrences
#                 patterns['recurring_expenses'].append({
#                     'amount': amount,
#                     'frequency': len(group),
#                     'description': group[0]['description']
#                 })
        
#         # Spending velocity
#         if len(expenses) >= 7:
#             recent_week = sum(e['amount'] for e in expenses[:7])
#             avg_weekly = sum(e['amount'] for e in expenses) / (len(expenses) / 7)
#             if recent_week > avg_weekly * 1.2:
#                 patterns['spending_velocity'] = 'increasing'
#             elif recent_week < avg_weekly * 0.8:
#                 patterns['spending_velocity'] = 'decreasing'
        
#         return patterns
    
#     def _create_forecast(self, expenses: List[Dict], category_breakdown: Dict) -> Dict:
#         # Simple forecast based on historical data
#         total_days = 90
#         total_spending = sum(e['amount'] for e in expenses)
#         daily_average = total_spending / total_days
        
#         forecast = {
#             'next_week': daily_average * 7,
#             'next_month': daily_average * 30,
#             'next_quarter': daily_average * 90,
#             'by_category': {}
#         }
        
#         # Category-specific forecasts
#         for cat, data in category_breakdown.items():
#             daily_cat_avg = data['total'] / total_days
#             forecast['by_category'][cat] = {
#                 'next_week': daily_cat_avg * 7,
#                 'next_month': daily_cat_avg * 30
#             }
        
#         return forecast
    
#     def _format_category_analysis(self, categories: Dict) -> str:
#         lines = []
#         for cat, data in sorted(categories.items(), key=lambda x: x[1]['total'], reverse=True):
#             lines.append(f"""
# {cat}:
#   Total: ${data['total']:.2f}
#   Transactions: {data['count']}
#   Average: ${data['average']:.2f}
#   Range: ${data['min']:.2f} - ${data['max']:.2f}""")
#         return "\n".join(lines)
    
#     def _format_patterns(self, patterns: Dict) -> str:
#         lines = []
        
#         if patterns['peak_spending_day']:
#             lines.append(f"Peak spending day: {patterns['peak_spending_day']['day']} (${patterns['peak_spending_day']['amount']:.2f})")
        
#         lines.append(f"Spending velocity: {patterns['spending_velocity']}")
        
#         if patterns['recurring_expenses']:
#             lines.append("\nRecurring expenses detected:")
#             for rec in patterns['recurring_expenses'][:3]:
#                 lines.append(f"  - ${rec['amount']:.2f} ({rec['frequency']} times) - {rec['description']}")
        
#         return "\n".join(lines)

# gemini_analyzer = GeminiExpenseAnalyzer()