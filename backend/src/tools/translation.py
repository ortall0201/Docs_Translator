# Temporarily simplified to avoid crewai_tools import issues
class TranslationTool:
    name: str = "Translation Tool"
    description: str = "Translates text between languages using mocked logic."

    def _run(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
        return f"[Translated from {source_lang} to {target_lang}]: {text}"
