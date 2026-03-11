from app.services.prompt_service import PromptService



def test_list_prompts_contains_expected_templates() -> None:
    service = PromptService()
    prompts = service.list_prompts()
    assert "summarize_text" in prompts
    assert "classify_issue" in prompts



def test_render_prompt_injects_variables() -> None:
    service = PromptService()
    rendered = service.render_prompt("summarize_text", {"text": "Observability matters."})
    assert "Observability matters." in rendered
