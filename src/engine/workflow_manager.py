import importlib
import inspect
from typing import Dict, Any


class WorkflowManager:
    def __init__(self, workflow_module='workflows'):
        self.workflow_module = workflow_module
        self.workflows: Dict[str, Any] = {}

    def load_workflow(self, workflow_name: str):
        if workflow_name not in self.workflows:
            try:
                module = importlib.import_module(f'{self.workflow_module}.{
                                                 workflow_name}_workflow')
                workflow_class = getattr(
                    module, f'{workflow_name.capitalize()}Workflow')
                self.workflows[workflow_name] = workflow_class()
            except (ImportError, AttributeError) as e:
                raise ValueError(f"Couldn't load workflow '{
                                 workflow_name}': {str(e)}")

    def execute_workflow(self, workflow_name: str, data: dict):
        self.load_workflow(workflow_name)
        return self.workflows[workflow_name].execute(data)
    
