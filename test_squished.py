import re

def test_squished():
    text = "applicationby UI componentsfor architectureand solutionfor Integrationwith APIsfor Developmentskills ensure100 and reduce manual planning effort by60"
    
    # Fix digits
    text = re.sub(r'([a-zA-Z])(\d+)', r'\1 \2', text)
    text = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', text)
    
    # Fix common stop words glued at the end
    glued_words = r'(skills|for|and|to|with|by|in|using|from)'
    text = re.sub(r'([a-z])' + glued_words + r'\b', r'\1 \2', text)
    
    print("Fixed:", text)

if __name__ == "__main__":
    test_squished()
