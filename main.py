import os
import time
from tavily import TavilyClient
from huggingface_hub import InferenceClient
from langchain_core.messages import HumanMessage

# Set API keys directly for testing
TAVILY_API_KEY = "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"
HUGGINGFACE_API_KEY = "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"
print("API Keys TAVILY_API_KEY:", TAVILY_API_KEY, "HUGGINGFACE_API_KEY:", HUGGINGFACE_API_KEY)

# Research and Data Collection Agent
class ResearchAgent:
    def __init__(self, search_terms):
        self.search_terms = search_terms
        self.client = TavilyClient(api_key=TAVILY_API_KEY)

    def search_web(self):
        query_string = " ".join(self.search_terms)
        print("Fixed Search Query:", query_string)
        gathered_data = self.client.search(query=query_string)
        return gathered_data

# Answer Drafter Agent
class AnswerDrafterAgent:
    def __init__(self, gathered_data):
        self.gathered_data = gathered_data
        self.client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

    def draft_answer(self):
        extracted_content = "\n\n".join(
            [result["content"] for result in self.gathered_data["results"] if "content" in result]
        )
        prompt = f"Summarize the following:\n{extracted_content}"
        print("Prompt:", prompt)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.text_generation(prompt, model="HuggingFaceH4/zephyr-7b-beta")
                return response
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    raise e
        return "The model is currently busy. Please try again later."

# Main System
class DeepResearchAI:
    def __init__(self, search_terms):
        self.search_terms = search_terms

    def run(self):
        research_agent = ResearchAgent(self.search_terms)
        gathered_data = research_agent.search_web()

        answer_drafter_agent = AnswerDrafterAgent(gathered_data)
        answer = answer_drafter_agent.draft_answer()

        return answer

# Example usage
search_terms = ["top headlines form times of india"]
deep_research_ai = DeepResearchAI(search_terms)
answer = deep_research_ai.run()
print("\nGenerated Answer:\n", answer)

 


