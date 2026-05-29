import os

def load_skill(skill_name: str) -> str:
    """
    Load a markdown skill file by name.
    Example: load_skill("rewriter") loads skills/prompts/rewriter.md
    """
    skill_path = os.path.join(
        os.path.dirname(__file__),
        "prompts",
        f"{skill_name}.md"
    )

    if not os.path.exists(skill_path):
        raise FileNotFoundError(f"Skill not found: {skill_path}")

    with open(skill_path, "r") as skill_file:
        return skill_file.read()