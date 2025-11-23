import os
import json
import logging
from fpdf import FPDF

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RoadmapGenerator")

class RoadmapGenerator:
    def __init__(self, output_dir: str = "outputs/roadmaps"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Simple resource database
        self.resources = {
            "Python": [
                {"title": "Python for Everybody (Coursera)", "url": "https://www.coursera.org/specializations/python", "type": "Course"},
                {"title": "Real Python Tutorials", "url": "https://realpython.com/", "type": "Article"}
            ],
            "SQL": [
                {"title": "SQLBolt", "url": "https://sqlbolt.com/", "type": "Interactive"},
                {"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "Tutorial"}
            ],
            "Data Engineer": [
                {"title": "Data Engineering Zoomcamp", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp", "type": "Course"},
                {"title": "Designing Data-Intensive Applications", "url": "https://dataintensive.net/", "type": "Book"}
            ],
            "Data Scientist": [
                {"title": "Machine Learning by Andrew Ng", "url": "https://www.coursera.org/learn/machine-learning", "type": "Course"},
                {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn", "type": "Interactive"}
            ],
            "Backend Engineer": [
                {"title": "The System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "type": "Guide"},
                {"title": "Django for Beginners", "url": "https://djangoforbeginners.com/", "type": "Book"}
            ]
        }

    def generate_roadmap(self, student_id: str, role: str, missing_skills: list):
        logger.info(f"Generating roadmap for {student_id} -> {role}")
        
        roadmap = {
            "student_id": student_id,
            "target_role": role,
            "duration_weeks": 12,
            "modules": []
        }
        
        # 1. Core Role Resources
        role_resources = self.resources.get(role, [])
        if role_resources:
            roadmap["modules"].append({
                "week": "1-4",
                "topic": f"Foundations of {role}",
                "resources": role_resources
            })
            
        # 2. Skill Gaps
        current_week = 5
        for skill in missing_skills:
            # Normalize skill name to match keys if needed
            # For now, simple lookup
            skill_key = next((k for k in self.resources if k.lower() == skill.lower()), None)
            if skill_key:
                roadmap["modules"].append({
                    "week": f"{current_week}-{current_week+1}",
                    "topic": f"Learn {skill_key}",
                    "resources": self.resources[skill_key]
                })
                current_week += 2
                
        # 3. Capstone
        roadmap["modules"].append({
            "week": "11-12",
            "topic": "Capstone Project",
            "description": f"Build a complete {role} project using {', '.join(missing_skills[:3])}."
        })
        
        # Save JSON
        json_path = os.path.join(self.output_dir, f"{student_id}.json")
        with open(json_path, 'w') as f:
            json.dump(roadmap, f, indent=2)
            
        # Generate PDF
        self.generate_pdf(roadmap, os.path.join(self.output_dir, f"{student_id}.pdf"))
        
        return roadmap

    def generate_pdf(self, roadmap: dict, filepath: str):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=f"Learning Roadmap: {roadmap['target_role']}", ln=1, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Student ID: {roadmap['student_id']}", ln=1)
        pdf.cell(200, 10, txt=f"Duration: {roadmap['duration_weeks']} Weeks", ln=1)
        
        pdf.ln(10)
        for module in roadmap['modules']:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt=f"Week {module.get('week', '?')}: {module['topic']}", ln=1)
            
            pdf.set_font("Arial", size=12)
            if 'description' in module:
                pdf.multi_cell(0, 10, txt=module['description'])
            
            if 'resources' in module:
                for res in module['resources']:
                    pdf.cell(200, 10, txt=f"- {res['title']} ({res['type']})", ln=1)
                    # pdf.cell(200, 10, txt=f"  {res['url']}", ln=1) # URL might be too long
            
            pdf.ln(5)
            
        pdf.output(filepath)
        logger.info(f"Saved PDF roadmap to {filepath}")

if __name__ == "__main__":
    gen = RoadmapGenerator()
    gen.generate_roadmap("test_student", "Data Engineer", ["Python", "SQL"])
