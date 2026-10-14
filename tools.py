from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
import wikipedia
import requests

from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime

# Configure Wikipedia User-Agent
session = requests.Session()
session.headers.update({
    "User-Agent": "MyResearchAgent/1.0 (contact: 0112al241041@bistbpl.in)"
})

wikipedia.wikipedia.requests = session


def save_to_txt(data: str, filename: str = "ressearch_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    formatted_text = (
        f"--- Research Output ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"{data}\n\n"
    )

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)

    return f"Data successfully saved to {filename}"


save_tool = Tool(
    name="save_to_txt",
    func=save_to_txt,
    description="Saves the research output to a text file"
)

search = DuckDuckGoSearchRun()

search_tool = Tool(
    name="search",
    func=search.run,
    description="Searches the web for current information"
)

api_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=100
)

wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
