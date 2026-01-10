from groq import Groq
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


def generate_documentation(parsed_code: Dict[str, Any]) -> Dict[str, Any]:
    if "error" in parsed_code:
        return {"error": "Cannot generate documentation for invalid code"}

    prompt = _build_prompt(parsed_code)
    docs = _call_groq(prompt)

    if docs.startswith("[ERROR]"):
        return {"error": docs}

    return {
        "readme": docs,
        "metadata": {
            "functions_documented": parsed_code["total_functions"],
            "classes_documented": parsed_code["total_classes"]
        }
    }


def _build_prompt(parsed_code: Dict[str, Any]) -> str:
    prompt = "Generate a professional README for Python code with the following structure : \n"

    prompt += "## Functions \n"

    if parsed_code["total_functions"] > 0:
        for func in parsed_code["functions"]:
            func_name = func["name"]
            params = ", ".join(func["params"])

            prompt += f" - {func_name}({params})\n"
            if func["docstring"]:
                prompt += f"Docstring : {func['docstring']}\n"
    else:
        prompt += " - None\n"

    prompt += "\n"

    prompt += "## Classes \n"

    if parsed_code["total_classes"] > 0:
        for cls in parsed_code["classes"]:
            prompt += f" - {cls['name']}\n"
            if cls["methods"]:
                for method in cls["methods"]:
                    method_params = ", ".join(method["params"])
                    prompt += f" - {method['name']}({method_params})\n"

                    if method["docstring"]:
                        prompt += f"Docstring : {method['docstring']}\n"

    else:
        prompt += " - None\n"

    prompt += "\n"
    prompt += """
                Please create a README with : 
                1. **Project Description**: Brief overview of what this code does
                2. **Installation**: How to install/setup
                3. **Usage**: Code examples showing how to use each function/class
                4. **API Reference**: Brief description of each function with parameters

                Keep it professional and concise. Use markdown formatting.
            """

    return prompt


def _call_groq(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Error : GROQ_API_KEY environment variable not set"

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical documentation expert. Generate clear, professional README files."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        documentation = response.choices[0].message.content

        return documentation

    except Exception as e:
        return f"[ERROR] {str(e)}"
