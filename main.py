"""
Question 12: Function Calling - FastAPI Endpoint

This endpoint maps queries to predefined functions.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define available functions
FUNCTIONS = [
    {
        "name": "get_ticket_status",
        "description": "Get the status of an IT support ticket",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "integer",
                    "description": "The ticket ID number"
                }
            },
            "required": ["ticket_id"]
        }
    },
    {
        "name": "schedule_meeting",
        "description": "Schedule a meeting on a specific date, time, and room",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Meeting date in YYYY-MM-DD format"
                },
                "time": {
                    "type": "string",
                    "description": "Meeting time in HH:MM format (24-hour)"
                },
                "meeting_room": {
                    "type": "string",
                    "description": "Meeting room identifier"
                }
            },
            "required": ["date", "time", "meeting_room"]
        }
    },
    {
        "name": "get_expense_balance",
        "description": "Get the expense reimbursement balance for an employee",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "The employee ID number"
                }
            },
            "required": ["employee_id"]
        }
    },
    {
        "name": "calculate_performance_bonus",
        "description": "Calculate the performance bonus for an employee for a specific year",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "The employee ID number"
                },
                "current_year": {
                    "type": "integer",
                    "description": "The year for bonus calculation"
                }
            },
            "required": ["employee_id", "current_year"]
        }
    },
    {
        "name": "report_office_issue",
        "description": "Report an office issue by issue code and department",
        "parameters": {
            "type": "object",
            "properties": {
                "issue_code": {
                    "type": "integer",
                    "description": "The issue code number"
                },
                "department": {
                    "type": "string",
                    "description": "The department name"
                }
            },
            "required": ["issue_code", "department"]
        }
    }
]


@app.get("/execute")
async def execute_function(q: str):
    """
    Map query to function call using OpenAI.
    
    Args:
        q: Natural language query
        
    Returns:
        Function name and arguments
    """
    try:
        # Call OpenAI with function calling
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that maps user queries to function calls. Extract parameters accurately from the query."
                },
                {
                    "role": "user",
                    "content": q
                }
            ],
            tools=[{"type": "function", "function": f} for f in FUNCTIONS],
            tool_choice="auto"
        )
        
        # Extract function call
        message = response.choices[0].message
        
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments
            
            return {
                "name": function_name,
                "arguments": arguments
            }
        else:
            raise HTTPException(status_code=400, detail="Could not map query to function")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Function Calling API - GET /execute?q=..."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
