from script_generator.script_generator import generate_script


def test_generate_script(monkeypatch):
    def fake_llm(prompt: str, *args, **kwargs) -> str:
        return "This is a generated script about cats boxing."

    # replace the LLM call with our fake function at runtime
    monkeypatch.setattr(
        "script_generator.script_generator._call_ollama",
        fake_llm,
    )

    script = generate_script("cats boxing")
    assert isinstance(script, str)
    assert "cats" in script.lower()
    assert "boxing" in script.lower()


def test_generate_script_rejects_empty_topic():
    try:
        generate_script("")
        assert False, "Expected ValueError"
    except ValueError:
        pass
