import os
import json
import pandas as pd
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SkillRoleMapper")

class SkillRoleMapper:
    def __init__(self, parsed_data_path: str = "data/jobs/parsed/jobs.json", output_dir: str = "models"):
        self.parsed_data_path = parsed_data_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def map_skills(self):
        logger.info("Loading parsed job data...")
        if not os.path.exists(self.parsed_data_path):
            logger.error(f"Parsed data not found at {self.parsed_data_path}")
            return

        with open(self.parsed_data_path, 'r', encoding='utf-8') as f:
            jobs = json.load(f)

        # 1. Compute Skill Frequency by Role
        role_skill_counts = defaultdict(lambda: defaultdict(int))
        role_counts = defaultdict(int)

        for job in jobs:
            # Extract role from title (simple heuristic for mock data)
            # In real scenario, we might use a classifier or more complex logic
            title = job.get('title', 'Unknown')
            # Simplify title to base role if possible (e.g., "Senior Data Engineer" -> "Data Engineer")
            # For mock data, titles are like "Senior Data Engineer"
            role = "Unknown"
            if "Data Engineer" in title: role = "Data Engineer"
            elif "Data Scientist" in title: role = "Data Scientist"
            elif "Backend" in title: role = "Backend Engineer"
            elif "Frontend" in title: role = "Frontend Engineer"
            elif "DevOps" in title: role = "DevOps Engineer"
            
            role_counts[role] += 1
            for skill in job.get('extracted_skills', []):
                role_skill_counts[role][skill] += 1

        # 2. Compute Probabilities P(skill|role) and P(role|skill)
        # We want to know: Given a skill, how likely is it associated with a role?
        # And: Given a role, how important is this skill?
        
        data = []
        all_skills = set()
        for role, skills in role_skill_counts.items():
            for skill, count in skills.items():
                all_skills.add(skill)
                
        for role in role_counts:
            for skill in all_skills:
                count = role_skill_counts[role].get(skill, 0)
                role_total = role_counts[role]
                
                # P(skill|role) = count(skill, role) / count(role)
                p_skill_given_role = count / role_total if role_total > 0 else 0
                
                data.append({
                    "role": role,
                    "skill": skill,
                    "count": count,
                    "p_skill_given_role": p_skill_given_role
                })
                
        df = pd.DataFrame(data)
        
        # Save matrix
        matrix_path = os.path.join(self.output_dir, "role_skill_matrix.csv")
        df.to_csv(matrix_path, index=False)
        logger.info(f"Saved role-skill matrix to {matrix_path}")
        
        # Save examples by role
        examples = defaultdict(list)
        for job in jobs:
             title = job.get('title', 'Unknown')
             role = "Unknown"
             if "Data Engineer" in title: role = "Data Engineer"
             elif "Data Scientist" in title: role = "Data Scientist"
             elif "Backend" in title: role = "Backend Engineer"
             elif "Frontend" in title: role = "Frontend Engineer"
             elif "DevOps" in title: role = "DevOps Engineer"
             
             if len(examples[role]) < 5:
                 examples[role].append(job['id'])
                 
        with open(os.path.join("data", "examples_by_role.json"), 'w') as f:
            json.dump(examples, f, indent=2)
        logger.info(f"Saved examples by role to data/examples_by_role.json")

if __name__ == "__main__":
    mapper = SkillRoleMapper()
    mapper.map_skills()
