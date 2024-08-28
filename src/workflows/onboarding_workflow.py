# src/workflows/onboarding_workflow.py

from tools.database_tool import DatabaseTool
from tools.log_tool import LogTool
from tools.extract_tool import ExtractTool


class OnboardingWorkflow:
    def __init__(self, db_tool: DatabaseTool, log_tool: LogTool, extract_tool: ExtractTool):
        self.db_tool = db_tool
        self.log_tool = log_tool
        self.extract_tool = extract_tool

    def execute(self, user_input: str) -> dict:
        try:
            # Extract user information
            name_result = self.extract_tool.execute(user_input, "name")
            email_result = self.extract_tool.execute(user_input, "email")

            if name_result["status"] == "error" or email_result["status"] == "error":
                raise ValueError("Unable to extract required information")

            name = name_result["extracted_info"]
            email = email_result["extracted_info"]

            # Create user in database
            user_data = {
                "name": name,
                "email": email,
                "onboarding_date": self.extract_tool.execute(user_input, "date")["extracted_info"]
            }
            db_result = self.db_tool.execute("insert_one", "users", user_data)

            if db_result["status"] == "error":
                raise ValueError(f"Database error: {db_result['message']}")

            # Log the successful onboarding
            log_result = self.log_tool.execute(
                f"User onboarded successfully",
                level="info",
                user_id=db_result["inserted_id"],
                name=name,
                email=email
            )

            return {
                "status": "success",
                "message": "User onboarded successfully",
                "user_id": db_result["inserted_id"],
                "name": name,
                "email": email
            }

        except Exception as e:
            error_message = f"Onboarding failed: {str(e)}"
            self.log_tool.execute(error_message, level="error")
            return {"status": "error", "message": error_message}

# Usage example:
# db_tool = DatabaseTool(mongo_handler)
# log_tool = LogTool()
# extract_tool = ExtractTool()
# onboarding = OnboardingWorkflow(db_tool, log_tool, extract_tool)
# result = onboarding.execute("My name is John Doe, email is john.doe@example.com, and I'm joining on 2023-06-15")
