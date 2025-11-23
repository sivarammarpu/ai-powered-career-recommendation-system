import os
import json
import time
import random
import datetime
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_collection.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DataCollector")

class JobScraper:
    def __init__(self, raw_data_dir: str = "data/jobs/raw"):
        self.raw_data_dir = raw_data_dir
        os.makedirs(self.raw_data_dir, exist_ok=True)
        
    def scrape(self, roles: List[str], count_per_role: int = 10):
        """
        Orchestrates the scraping process.
        """
        raise NotImplementedError("Subclasses must implement scrape method")

    def save_raw_job(self, job_data: Dict, source: str):
        """
        Saves a single job entry to a JSON file.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        job_id = job_data.get('id', f"unknown_{random.randint(1000,9999)}")
        filename = f"{source}_{job_id}_{timestamp}.json"
        filepath = os.path.join(self.raw_data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, indent=2)
        
        # logger.info(f"Saved job {job_id} to {filepath}")

class MockJobScraper(JobScraper):
    """
    Generates synthetic job data for testing and development.
    """
    def __init__(self, raw_data_dir: str = "data/jobs/raw"):
        super().__init__(raw_data_dir)
        self.skills_pool = {
            "Data Engineer": ["Python", "SQL", "Spark", "AWS", "Airflow", "Kafka", "ETL", "BigQuery"],
            "Data Scientist": ["Python", "Pandas", "Scikit-learn", "TensorFlow", "PyTorch", "Statistics", "SQL"],
            "Backend Engineer": ["Java", "Spring Boot", "Python", "Django", "PostgreSQL", "Docker", "Kubernetes", "Redis"],
            "Frontend Engineer": ["JavaScript", "React", "TypeScript", "CSS", "HTML", "Redux", "Webpack"],
            "DevOps Engineer": ["Linux", "Bash", "AWS", "Terraform", "Docker", "Kubernetes", "CI/CD", "Jenkins"]
        }
        self.seniority_levels = ["Junior", "Mid-Level", "Senior", "Lead", "Principal"]

    def generate_job_description(self, role: str, skills: List[str]) -> str:
        return f"""
        We are looking for a {role} to join our team.
        
        Responsibilities:
        - Design and implement scalable solutions.
        - Collaborate with cross-functional teams.
        - Maintain and improve existing codebases.
        
        Requirements:
        - Proficiency in {', '.join(random.sample(skills, k=min(3, len(skills))))}.
        - Experience with {', '.join(random.sample(skills, k=min(2, len(skills))))} is a plus.
        - Strong problem-solving skills.
        - Bachelor's degree in Computer Science or related field.
        """

    def scrape(self, roles: List[str], count_per_role: int = 10):
        logger.info(f"Starting mock scrape for roles: {roles}")
        total_scraped = 0
        
        for role in roles:
            logger.info(f"Generating {count_per_role} jobs for {role}...")
            relevant_skills = self.skills_pool.get(role, ["General Skills"])
            
            for i in range(count_per_role):
                job_id = f"mock_{role.replace(' ', '_')}_{random.randint(10000, 99999)}"
                seniority = random.choice(self.seniority_levels)
                
                job_data = {
                    "id": job_id,
                    "title": f"{seniority} {role}",
                    "company": f"MockCompany_{random.randint(1, 100)}",
                    "location": random.choice(["Remote", "New York, NY", "San Francisco, CA", "Bangalore, IN", "London, UK"]),
                    "description": self.generate_job_description(role, relevant_skills),
                    "posted_date": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).isoformat(),
                    "source": "mock_generator",
                    "url": f"https://example.com/jobs/{job_id}"
                }
                
                self.save_raw_job(job_data, "mock")
                total_scraped += 1
                
        logger.info(f"Mock scrape completed. Total jobs generated: {total_scraped}")

if __name__ == "__main__":
    # Example usage
    scraper = MockJobScraper()
    target_roles = ["Data Engineer", "Data Scientist", "Backend Engineer", "Frontend Engineer", "DevOps Engineer"]
    scraper.scrape(target_roles, count_per_role=20)
