# app/llm/llm_api.py

from openai import OpenAI
from typing import List, Dict

# Initialize the client
client = OpenAI(
    base_url="https://litellm.rillavoice.com/v1",
    api_key="sk-rilla-vibes"
)

def query_llm(code_blocks: List[Dict], rubric: Dict, model: str = "claude-3-5-haiku") -> Dict:
    """
    Send code and rubric to LLM and receive score, comments, suggestions.

    Args:
        code_blocks (List[Dict]): List of {"source": str, "outputs": List[str]}
        rubric (Dict): Grading rubric in structured form
        model (str): Model name

    Returns:
        Dict: {"score": int/float, "comments": str, "suggestions": str}
    """

    # Build prompt from code and rubric
    prompt = build_prompt(code_blocks, rubric)

    # Send to LLM
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse response
    content = response.choices[0].message.content

    return parse_response(content)


def build_prompt(code_blocks: List[Dict], rubric: Dict) -> str:
    code_str = "\n\n".join(
        f"Code:\n{block['source']}\nOutput:\n{''.join(block.get('outputs', []))}"
        for block in code_blocks
    )
    rubric_str = "\n".join(f"{key}: {value}" for key, value in rubric.items())

    prompt = f"""
You are an automated grader for Python notebook assignments.

Rubric:
{rubric_str}

Student Submission:
{code_str}

Please:
1. Give a score based on the rubric (0-100).
2. Comment on what was done correctly or incorrectly.
3. Suggest specific improvements.

Respond in JSON format like:
{{
  "score": int,
  "comments": "string",
  "suggestions": "string"
}}
"""
    return prompt.strip()


def parse_response(response_text: str) -> Dict:
    """
    Try to safely parse the response text into a Python dictionary.
    """
    import json
    import re

    # Find JSON blob in response
    try:
        json_text = re.search(r"\{.*\}", response_text, re.DOTALL).group()
        return json.loads(json_text)
    except Exception as e:
        return {
            "score": -1,
            "comments": "Failed to parse LLM response.",
            "suggestions": f"Raw output: {response_text}"
        }
