import os
import json
import pickle
import logging
from typing import List, Dict, Set
from collections import defaultdict
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ParserAndNLP")

class SkillExtractor:
    def __init__(self, raw_data_dir: str = "data/jobs/raw", output_dir: str = "data/skills", embeddings_dir: str = "data/embeddings"):
        self.raw_data_dir = raw_data_dir
        self.output_dir = output_dir
        self.embeddings_dir = embeddings_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.embeddings_dir, exist_ok=True)
        
        # Simple dictionary of skills for keyword matching (can be expanded or replaced with spaCy EntityRuler)
        self.common_skills = {
            "python", "java", "c++", "c#", "javascript", "typescript", "react", "angular", "vue",
            "sql", "nosql", "mongodb", "postgresql", "mysql", "oracle",
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible",
            "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
            "spark", "hadoop", "kafka", "airflow", "etl", "big data",
            "html", "css", "flask", "django", "spring boot", "node.js",
            "git", "linux", "bash", "agile", "scrum"
        }
        
        # Normalization mapping
        self.skill_aliases = {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "reactjs": "react",
            "aws cloud": "aws",
            "ml": "machine learning",
            "dl": "deep learning"
        }

    def normalize_skill(self, skill: str) -> str:
        skill = skill.lower().strip()
        return self.skill_aliases.get(skill, skill)

    def extract_skills(self, text: str) -> List[str]:
        """
        Extracts skills from text using simple keyword matching.
        """
        text_lower = text.lower()
        found_skills = set()
        
        # 1. Exact match from common_skills
        for skill in self.common_skills:
            # Simple regex to ensure word boundary
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.add(skill)
                
        # 2. Check for aliases
        for alias, canonical in self.skill_aliases.items():
             if re.search(r'\b' + re.escape(alias) + r'\b', text_lower):
                found_skills.add(canonical)
                
        return list(found_skills)

    def process_jobs(self):
        logger.info("Starting job processing...")
        job_files = [f for f in os.listdir(self.raw_data_dir) if f.endswith('.json')]
        
        all_jobs_data = []
        corpus = []
        job_ids = []
        skill_counts = defaultdict(int)
        skill_to_jobs = defaultdict(list)
        
        for job_file in job_files:
            with open(os.path.join(self.raw_data_dir, job_file), 'r', encoding='utf-8') as f:
                job = json.load(f)
                
            text = f"{job.get('title', '')} {job.get('description', '')}"
            skills = self.extract_skills(text)
            
            # Enrich job data
            job['extracted_skills'] = skills
            all_jobs_data.append(job)
            
            # For TF-IDF
            corpus.append(text)
            job_ids.append(job['id'])
            
            # Stats
            for skill in skills:
                skill_counts[skill] += 1
                skill_to_jobs[skill].append(job['id'])
                
        # Save parsed jobs (optional, or just keep in memory for next step if small)
        # We'll save a summary skill dict
        skill_dict = {
            "counts": dict(skill_counts),
            "mapping": dict(skill_to_jobs)
        }
        
        with open(os.path.join(self.output_dir, "skill_dict.json"), 'w') as f:
            json.dump(skill_dict, f, indent=2)
            
        logger.info(f"Saved skill dictionary to {os.path.join(self.output_dir, 'skill_dict.json')}")
        
        # Compute TF-IDF
        logger.info("Computing TF-IDF vectors...")
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Save TF-IDF model and matrix
        with open(os.path.join(self.embeddings_dir, "job_tfidf.pkl"), 'wb') as f:
            pickle.dump({
                "vectorizer": vectorizer,
                "matrix": tfidf_matrix,
                "job_ids": job_ids
            }, f)
            
        logger.info(f"Saved TF-IDF data to {os.path.join(self.embeddings_dir, 'job_tfidf.pkl')}")
        
        # Also save the parsed jobs with extracted skills for the next step
        parsed_jobs_path = os.path.join("data/jobs/parsed", "jobs.json")
        with open(parsed_jobs_path, 'w') as f:
            json.dump(all_jobs_data, f, indent=2)
        logger.info(f"Saved parsed jobs to {parsed_jobs_path}")

if __name__ == "__main__":
    parser = SkillExtractor()
    parser.process_jobs()
