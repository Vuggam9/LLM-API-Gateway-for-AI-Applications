from pathlib import Path


class PromptService:
    def __init__(self) -> None:
        self.prompts_dir = Path(__file__).resolve().parent.parent / "prompts"

    def list_prompts(self) -> list[str]:
        return sorted(path.stem for path in self.prompts_dir.glob("*.txt"))

    def load_template(self, template_name: str) -> str:
        template_path = self.prompts_dir / f"{template_name}.txt"
        if not template_path.exists():
            raise FileNotFoundError(f"Prompt template '{template_name}' was not found.")
        return template_path.read_text(encoding="utf-8")

    def render_prompt(self, template_name: str, input_variables: dict[str, object]) -> str:
        template = self.load_template(template_name)
        return template.format(**input_variables)
