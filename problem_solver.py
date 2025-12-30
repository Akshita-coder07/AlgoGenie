from autogen_agentchat.agents import AssistantAgent
from config.settings import get_model_client

model_client = get_model_client()

def get_problem_solver_agent():
    """
    Function to get the problem solver agent.
    This agent is responsible for solving DSA problems.
    It will work with the code executor agent to execute the code.
    """
    
    problem_solver_agent = AssistantAgent(
        name="DSA_Problem_Solver",
        description="An expert DSA problem solver",
        model_client=model_client,
        system_message="""You are an expert DSA problem solver.

WORKFLOW (strictly follow):

Message 1: Brief plan (2-3 lines) + Solution code with 3 test cases
Message 2: Analyze execution results + File save code
Message 3: Say "STOP"

Code format for saving:
```python
solution_code = '''
def your_function():
    # your code here
    pass
'''
with open("solution.py", "w") as f:
    f.write(solution_code)
print("✅ Solution saved to solution.py")
```

Rules:
- ONE code block per message
- Wait for CodeExecutor between messages  
- Do NOT say STOP until solution.py is saved
        """
    )
    
    return problem_solver_agent