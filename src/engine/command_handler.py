class CommandHandler:
    def __init__(self, workflow_manager: WorkflowManager):
        self.workflow_manager = workflow_manager

    def handle_command(self, node: str, data: dict):
        try:
            result = self.workflow_manager.execute_workflow(node, data)
            return {"status": "success", "data": result}
        except ValueError as e:
            return {"status": "error", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}
