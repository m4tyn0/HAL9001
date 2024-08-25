from typing import Dict, Any

class SkillTool:
    name = "add_skill"

    def __call__(self, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        data = tool_input["data"]
        command = tool_input["command"]

        skill_name = command["name"]
        skill_level = command["level"]

        # Check if skill already exists
        for skill in data["user"]["skills"]:
            if skill["name"] == skill_name:
                skill["level"] = skill_level
                skill["target"] = skill_level + 1
                return {"output": f"Updated skill: {skill_name} to level {skill_level}"}

        # Add new skill
        new_skill = {
            "name": skill_name,
            "level": skill_level,
            "target": skill_level + 1,
            "total_xp": 0
        }
        data["user"]["skills"].append(new_skill)

        return {"output": f"Added new skill: {skill_name} at level {skill_level}"}