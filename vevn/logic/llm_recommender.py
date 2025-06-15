import os
import json
import ollama

def load_career_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.normpath(os.path.join(script_dir, '..', 'data', 'careers.json'))
    with open(json_path, "r") as f:
        return json.load(f)

def get_llm_recommendations(user_input):
    careers = load_career_data()
    career_summaries = "\n".join(
        [f"{c['title']}: {c['description']} (Skills: {', '.join(c['skills'])})" for c in careers]
    )

    prompt = f"""
You are an AI career advisor. Based on this user's input:
"{user_input}"

Choose the best matching careers from this database:
{career_summaries}

Return 2-3 careers that best fit, with a short reason for each.
"""

    response = ollama.chat(
        model='mistral',  # or 'llama3', 'gemma', etc.
        messages=[
            {"role": "system", "content": "You are a helpful AI career advisor."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']
