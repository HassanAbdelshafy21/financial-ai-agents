from app.agents.agent import agent

def test_memory():
    # First message - give the agent some info
    response1 = agent.invoke({
        "messages": [("user", "My monthly income is $5000")]
    }, config={"configurable": {"thread_id": "test_123"}})
    
    print("First response:", response1["messages"][-1].content)
    
    # Second message - see if it remembers
    response2 = agent.invoke({
        "messages": [("user", "What's my income?")]
    }, config={"configurable": {"thread_id": "test_123"}})
    
    print("Second response:", response2["messages"][-1].content)

if __name__ == "__main__":
    test_memory()