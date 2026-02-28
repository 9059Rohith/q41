# Question 12: Function Calling API

## Setup

```bash
cd q12_function_calling
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
```

## Run

```bash
python main.py
```

## Test

```bash
curl "http://localhost:8000/execute?q=What%20is%20the%20status%20of%20ticket%2083742?"
```

## Response

```json
{
  "name": "get_ticket_status",
  "arguments": "{\"ticket_id\": 83742}"
}
```

## Available Functions

1. `get_ticket_status(ticket_id: int)`
2. `schedule_meeting(date: str, time: str, meeting_room: str)`
3. `get_expense_balance(employee_id: int)`
4. `calculate_performance_bonus(employee_id: int, current_year: int)`
5. `report_office_issue(issue_code: int, department: str)`

## Notes

- Uses OpenAI function calling
- Arguments in same order as function definition
- CORS enabled for cross-origin requests
