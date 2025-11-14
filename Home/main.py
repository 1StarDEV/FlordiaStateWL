import os
from typing import Dict, List, Optional

# NOTE: This code uses the Google GenAI SDK approach. 
# To run this script, you would need to install the SDK: pip install google-genai
# and set up your API Key: os.environ['GEMINI_API_KEY'] = 'YOUR_API_KEY'

# --- Configuration (Mocking the required imports for demonstration) ---
# We use mock classes/functions to demonstrate the structure without needing 
# to install external dependencies in this execution environment.

class MockTool:
    """Represents a mock tool for the SDK (e.g., google_search)."""
    def __init__(self, name):
        self.name = name

class MockConfig:
    """Represents mock configuration for the SDK (system instructions, tools)."""
    def __init__(self, system_instruction: str, tools: Optional[List[MockTool]] = None):
        self.system_instruction = system_instruction
        self.tools = tools

class MockClient:
    """
    Represents a mock client for the Gemini API. 
    In a real environment, this would be 'client = genai.Client()'.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        print("--- Initializing Mock Gemini Client ---")

    def generate_content(self, model: str, contents: str, config: MockConfig) -> Dict:
        """
        Simulates calling the Gemini API to generate content and return a structured response.
        
        Args:
            model: The model name (e.g., 'gemini-2.5-flash').
            contents: The user's prompt/query.
            config: The generation configuration (system prompt, tools).
            
        Returns:
            A dictionary simulating the API response, including text and (optionally) sources.
        """
        print(f"\n[MOCK API CALL] Model: {model}")
        print(f"[MOCK API CALL] Query: '{contents}'")
        print(f"[MOCK API CALL] System Instruction: '{config.system_instruction[:50]}...'")

        if config.tools and config.tools[0].name == "google_search":
            # Simulation for Grounded Chat (e.g., "What are the core departments?")
            return {
                "text": (
                    "FSRPWL (Florida State Roleplay Whitelisted) is a highly structured "
                    "roleplay community focused on the **Emergency Response: Liberty County** game on Roblox. "
                    "We emphasize maturity, realism, and adherence to realistic procedures. "
                    "Here is a table of our core departments:\n\n"
                    "| Department | Primary Focus |\n"
                    "|---|---|\n"
                    "| FHP | Interstate enforcement & traffic |\n"
                    "| Sheriff's Office | Patrol, investigations, community policing |\n"
                    "| Fire & Rescue | Medical, fire suppression, technical rescue |\n"
                    "| Communications | Call taking & unit coordination |\n\n"
                    "If you'd like to dive deeper into any department, just ask!"
                ),
                "sources": [
                    {"title": "FSRPWL Community Guidelines", "uri": "https://example.com/fsrpwl-rules"},
                    {"title": "Roblox ER:LC Wiki", "uri": "https://example.com/erlc-wiki"}
                ]
            }
        else:
            # Simulation for Creative Scenario Generation (e.g., for Sheriff's Office)
            return {
                "text": (
                    "**Scenario: Armed Robbery in Progress.** You are a Sheriff's Office deputy responding to a 211 (Armed Robbery) at the County Bank branch. "
                    "Dispatch reports two suspects inside with handguns. Multiple 911 calls confirm that hostages have been taken. "
                    "Your primary directive is to establish a secure perimeter, contain the suspects, and coordinate with specialized units (SWAT) as they arrive on scene. **Do not engage alone.** Your decisions on prioritizing life safety vs. containment are crucial."
                ),
                "sources": []
            }


# --- Core AI Functions ---

# Use the mock client
gemini_client = MockClient(api_key=os.environ.get('GEMINI_API_KEY'))


def generate_chat_response(user_query: str) -> Dict[str, str | List[Dict[str, str]]]:
    """
    Generates a conversational and grounded response for the FSRPWL chatbot.
    
    This function simulates the use of the Google Search grounding tool.
    """
    system_prompt = (
        "You are Flordiee AI, a helpful and professional assistant for the FSRPWL "
        "community. You are friendly and knowledgeable. You MUST use factual, "
        "search-grounded information when possible."
    )
    
    # Configuration for search grounding
    config = MockConfig(
        system_instruction=system_prompt,
        tools=[MockTool(name="google_search")] 
    )

    api_response = gemini_client.generate_content(
        model='gemini-2.5-flash',
        contents=user_query,
        config=config
    )
    
    return {
        "text": api_response["text"],
        "sources": api_response.get("sources", [])
    }


def generate_rp_scenario(department: str) -> str:
    """
    Generates a creative roleplay scenario for a specific department (no grounding).
    """
    system_prompt = (
        "You are a creative director for a realistic, mature, whitelist-only roleplay "
        "community. Your job is to generate engaging, serious, and realistic scenario prompts "
        "for players, suitable for a mature audience."
    )
    query = f"Generate a short, realistic roleplay scenario (around 100 words) for the '{department}' department."

    # Configuration without tools for creative output
    config = MockConfig(system_instruction=system_prompt)

    api_response = gemini_client.generate_content(
        model='gemini-2.5-flash',
        contents=query,
        config=config
    )

    return api_response["text"]


# --- Demonstration ---

if __name__ == "__main__":
    print("--- FSRPWL AI Tool Demonstration ---")
    
    # 1. Demo Chatbot (Grounded Response, includes simulated table)
    chat_query = "What are the core departments in FSRPWL?"
    print(f"\n[DEMO 1] Chatbot Query: {chat_query}")
    
    chat_response = generate_chat_response(chat_query)
    
    print("\n--- AI Chat Response (Grounded) ---")
    print(chat_response['text'])
    if chat_response['sources']:
        print("\nSources Used:")
        for source in chat_response['sources']:
            print(f"- {source['title']}: {source['uri']}")

    print("\n" + "="*50 + "\n")

    # 2. Demo Scenario Generator (Creative Response)
    department_choice = "Sheriff's Office"
    print(f"[DEMO 2] Scenario Request for: {department_choice}")
    
    scenario = generate_rp_scenario(department_choice)
    
    print("\n--- AI Scenario Response (Creative) ---")
    print(scenario)
    
    print("\n--- Demonstration Complete ---")
