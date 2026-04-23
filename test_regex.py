import re

def test_regex():
    texts = [
        "Programming LanguagesJava, Kotlin",
        "ToolsAndroid Studio, Git",
        "ReactJS",
        "iOS",
        "macOS",
        "CI/CD",
        "C++",
        "Next.js",
        "REST APIs"
    ]
    
    for t in texts:
        # Add space between lowercase and uppercase
        new_t = re.sub(r'([a-z])([A-Z])', r'\1 \2', t)
        print(f"{t:35} -> {new_t}")

if __name__ == "__main__":
    test_regex()
