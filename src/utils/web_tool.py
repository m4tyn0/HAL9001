from langgraph.prebuilt import Tool
import aiohttp


class WebTool(Tool):
    def __init__(self):
        super().__init__(
            name="WebTool",
            description="Tool for interacting with web resources",
            function=self.execute
        )

    async def execute(self, url: str, method: str = "GET", data: dict = None):
        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(url) as response:
                    return {"status": "success", "content": await response.text()}
            elif method == "POST":
                async with session.post(url, json=data) as response:
                    return {"status": "success", "content": await response.text()}
            else:
                return {"status": "error", "message": "Unsupported HTTP method"}
