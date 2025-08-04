from flask import Flask, render_template, request

app = Flask(__name__)

# Database of careers and their required skills
career_paths = {
    "data_scientist": ["python", "statistics", "machine_learning", "data_visualization", "sql"],
    "web_developer": ["javascript", "html", "css", "react", "nodejs"],
    "cybersecurity": ["networking", "linux", "ethical_hacking", "cryptography", "python"],
}

# Available courses mapped to skills they teach
courses = {
    "python_basics": {"skills": ["python"], "level": "beginner"},
    "python_advanced": {"skills": ["python"], "level": "intermediate"},
    "intro_stats": {"skills": ["statistics"], "level": "beginner"},
    "ml_fundamentals": {"skills": ["machine_learning"], "level": "intermediate"},
    "data_viz": {"skills": ["data_visualization"], "level": "intermediate"},
    "sql_course": {"skills": ["sql"], "level": "beginner"},
    "js_crash_course": {"skills": ["javascript"], "level": "beginner"},
    "html_css": {"skills": ["html", "css"], "level": "beginner"},
    "react_course": {"skills": ["react"], "level": "intermediate"},
    "nodejs": {"skills": ["nodejs"], "level": "intermediate"},
    "networking_101": {"skills": ["networking"], "level": "beginner"},
    "linux_basics": {"skills": ["linux"], "level": "beginner"},
    "ethical_hacking": {"skills": ["ethical_hacking"], "level": "advanced"},
    "crypto_intro": {"skills": ["cryptography"], "level": "intermediate"},
}

# Learning resources for each course
resources = {
    "python_basics": ["Python for Beginners book", "Python Basics YouTube Series"],
    "intro_stats": ["Statistics Fundamentals online course", "Stats Practice Problems"],
    "ml_fundamentals": ["Machine Learning with Python course", "ML Practice Projects"],
    "data_viz": ["Data Visualization with Matplotlib", "Tableau Tutorials"],
    "sql_course": ["SQL for Beginners", "Interactive SQL Practice"],
    "js_crash_course": ["JavaScript.info", "Codecademy JavaScript"],
    "html_css": ["HTML & CSS Design book", "FreeCodeCamp Responsive Design"],
    "react_course": ["Official React Documentation", "React Tutorial Projects"],
    "nodejs": ["Node.js Getting Started", "Express.js Guide"],
    "networking_101": ["Networking Fundamentals", "Cisco Networking Academy"],
    "linux_basics": ["Linux Command Line Basics", "Linux Administration Handbook"],
    "ethical_hacking": ["Hacking: The Art of Exploitation", "TryHackMe"],
    "crypto_intro": ["Cryptography I (Coursera)", "Applied Cryptography"]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        current_skills = request.form.get('current_skills', '').lower().split(',')
        target_career = request.form.get('target_career', '').lower()
        current_level = request.form.get('current_level', '').lower()
        
        # Process the data
        recommendations = generate_recommendations(
            [skill.strip() for skill in current_skills],
            target_career.strip(),
            current_level.strip()
        )
        
        return render_template('index.html', 
                             recommendations=recommendations,
                             form_data=request.form)
    
    return render_template('index.html')

def generate_recommendations(current_skills, target_career, current_level):
    target_skills = career_paths.get(target_career, [])
    
    if not target_skills:
        return {"error": "Sorry, we don't have information about that career path yet."}
    
    # Identify skills the user needs to learn
    needed_skills = [skill for skill in target_skills 
                     if skill not in current_skills]
    
    if not needed_skills:
        return {"message": "You already have all the required skills for this career path!"}
    
    # Recommend courses for needed skills
    recommended_courses = []
    for skill in needed_skills:
        for course, details in courses.items():
            if skill in details["skills"]:
                # Simple level matching
                if (details["level"] == "beginner" or 
                    (details["level"] == "intermediate" and current_level != "beginner") or
                    (details["level"] == "advanced" and current_level == "advanced")):
                    recommended_courses.append(course)
    
    # Get unique courses
    recommended_courses = list(set(recommended_courses))
    
    # Generate learning path with resources
    learning_path = []
    for course in recommended_courses:
        learning_path.append({
            "course": course.replace('_', ' ').title(),
            "skills_covered": ", ".join(courses[course]["skills"]),
            "resources": resources.get(course, ["General online search for: " + course.replace('_', ' ')])
        })
    
    return {
        "career": target_career.replace('_', ' ').title(),
        "learning_path": learning_path
    }

if __name__ == '__main__':
    app.run(debug=True)