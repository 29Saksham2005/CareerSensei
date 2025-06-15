# logic/recommender.py

def get_recommendations(interests, skills, education):
    careers = []

    # Simple keyword-based mapping (expand later)
    if "technology" in interests.lower() or "coding" in skills.lower():
        careers.append({
            "title": "Software Developer",
            "description": "Builds apps, websites, and systems.",
            "growth": "High"
        })

    if "design" in interests.lower():
        careers.append({
            "title": "UI/UX Designer",
            "description": "Creates user-friendly interfaces.",
            "growth": "Medium"
        })

    if "biology" in interests.lower() or "medical" in skills.lower():
        careers.append({
            "title": "Biotech Researcher",
            "description": "Works on health and bio-solutions.",
            "growth": "Growing field"
        })

    if not careers:
        careers.append({
            "title": "Generalist",
            "description": "Explore various fields with internships or online courses.",
            "growth": "Depends on path"
        })

    return careers
