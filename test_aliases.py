import re

def expand_aliases():
    base_skills = ["JavaScript", "TypeScript", "GitHub", "GitLab", "LinkedIn", "iOS", "macOS"]
    
    variations = set(base_skills)
    for skill in base_skills:
        # Handle CamelCase (JavaScript -> Java Script)
        camel_split = re.sub(r'(?<![im])([a-z])([A-Z])', r'\1 \2', skill)
        if camel_split != skill:
            variations.add(camel_split)
            
    for v in variations:
        print(v)

if __name__ == "__main__":
    expand_aliases()
