# src/tools/log_tool.py

from langgraph.prebuilt import Tool
import logging
from datetime import datetime


class LogTool(Tool):
    def __init__(self, log_file='app.log'):
        super().__init__(
            name="LogTool",
            description="Tool for logging messages and actions",
            function=self.execute
        )
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def execute(self, message: str, level: str = "info", **kwargs) -> dict:
        log_method = getattr(self.logger, level.lower(), self.logger.info)

        # Include any additional context in the log message
        context = ' '.join(f'{k}={v}' for k, v in kwargs.items())
        full_message = f"{message} - {context}" if context else message

        log_method(full_message)

        return {
            "status": "success",
            "message": "Log entry created",
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "content": full_message
        }

# Usage example:
# log_tool = LogTool()
# result = log_tool.execute("User logged in", level="info", user_id="123", ip_address="192.168.1.1")
