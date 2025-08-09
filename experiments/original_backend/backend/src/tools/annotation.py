from crewai_tools import BaseTool

class AnnotationTool(BaseTool):
    name: str = "Annotation Tool"
    description: str = "Explains key form fields using a static glossary."

    def _run(self, field_name: str) -> str:
        glossary = {
            "PESEL": "Polish national identification number.",
            "Zameldowanie": "Official registration of place of residence."
        }
        return glossary.get(field_name, "No extra info available.")
