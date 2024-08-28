# src/tools/extract_tool.py

from langgraph.prebuilt import Tool
import re


class ExtractTool(Tool):
    def __init__(self):
        super().__init__(
            name="ExtractTool",
            description="Tool for extracting information from text",
            function=self.execute
        )

    def execute(self, text: str, extract_type: str) -> dict:
        if extract_type == "name":
            return self._extract_name(text)
        elif extract_type == "email":
            return self._extract_email(text)
        elif extract_type == "date":
            return self._extract_date(text)
        else:
            return {"status": "error", "message": f"Unsupported extraction type: {extract_type}"}

    def _extract_name(self, text: str) -> dict:
        # Simple regex to extract names (assumes names are 2-3 words, each starting with a capital letter)
        match = re.search(r'\b([A-Z][a-z]+ ){1,2}[A-Z][a-z]+\b', text)
        if match:
            return {"status": "success", "extracted_info": match.group().strip()}
        return {"status": "error", "message": "Unable to extract name"}

    def _extract_email(self, text: str) -> dict:
        # Simple regex to extract email addresses
        match = re.search(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if match:
            return {"status": "success", "extracted_info": match.group()}
        return {"status": "error", "message": "Unable to extract email"}

    def _extract_date(self, text: str) -> dict:
        # Simple regex to extract dates in format YYYY-MM-DD
        match = re.search(r'\d{4}-\d{2}-\d{2}', text)
        if match:
            return {"status": "success", "extracted_info": match.group()}
        return {"status": "error", "message": "Unable to extract date"}

# Usage example:
# extract_tool = ExtractTool()
# result = extract_tool.execute("My name is John Doe and my email is john.doe@example.com", "name")
# result = extract_tool.execute("My name is John Doe and my email is john.doe@example.com", "email")
# result = extract_tool.execute("The meeting is scheduled for 2023-06-15", "date")
