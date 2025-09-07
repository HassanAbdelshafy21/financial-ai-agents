import httpx

BASE_URL = "http://localhost:8000"

def query_agent(query: str, thread_id: str = "default"):
    """
    Send a query to the AI agent and get a response.
    
    Args:
        query: The user's question/message
        thread_id: Conversation thread ID (to maintain memory)
    
    Returns:
        dict: Response from the API or error info
    """
    try:
        # Make the HTTP POST request
        response = httpx.post(
            f"{BASE_URL}/api/v1/query",  # The endpoint URL
            json={                       # Send data as JSON
                "query": query,
                "thread_id": thread_id
            },
            headers={                    # Required headers
                "Content-Type": "application/json"
            },
            timeout=30.0                 # Don't wait forever
        )
        
        # Check if request was successful
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def login(email: str, password: str):
    """
    Authenticate with the API and get a JWT token.
    
    Args:
        email: The user's email
        password: The user's password

    Returns:
        dict: Token info or error
    """
    try:
        response = httpx.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={
                "email": email,
                "password": password
            },
            headers={
                "Content-Type": "application/json"
            },
            timeout=30.0
        )

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}

    except Exception as e:
        return {"success": False, "error": str(e)}
def register(email: str, password: str, full_name: str):
    """
    Register a new user with the API.
    
    Args:
        email: The user's email
        password: The user's password
        full_name: The user's full name

    Returns:
        dict: Registration info or error
    """
    try:
        url = f"{BASE_URL}/api/v1/auth/register"
        data = {
            "email": email,
            "password": password,
            "full_name": full_name
        }
        
        print(f"Making request to: {url}")  # Debug print
        print(f"With data: {data}")        # Debug print
        
        response = httpx.post(
            url,
            json=data,
            headers={
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        
        print(f"Response status: {response.status_code}")  # Debug print
        print(f"Response body: {response.text}")           # Debug print

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}

    except Exception as e:
        print(f"Exception occurred: {e}")  # Debug print
        return {"success": False, "error": str(e)}
    
def create_chat(title: str, token: str):
    try:
        response = httpx.post(
            f"{BASE_URL}/api/v1/chats/",
            json={"title": title},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def save_message(chat_id: int, role: str, content: str, token: str):
    try:
        response = httpx.post(
            f"{BASE_URL}/api/v1/chats/{chat_id}/messages",
            json={"role": role, "content": content},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0
        )
        if response.status_code == 200:
            return {"success": True}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def generate_report(token: str):
    try:
        response = httpx.post(
            f"{BASE_URL}/api/v1/reports/generate",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0
        )
        if response.status_code == 200:
            return {"success": True, "data": response.content}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}