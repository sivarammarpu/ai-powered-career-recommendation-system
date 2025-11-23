import unittest
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser_nlp import SkillExtractor
from src.roadmap import RoadmapGenerator
from src.clustering import ProfileClustering

class TestAgents(unittest.TestCase):
    def test_skill_extraction(self):
        extractor = SkillExtractor()
        text = "We need a Python developer with SQL and AWS experience."
        skills = extractor.extract_skills(text)
        self.assertIn("python", skills)
        self.assertIn("sql", skills)
        self.assertIn("aws", skills)
        
    def test_roadmap_generation(self):
        generator = RoadmapGenerator(output_dir="tests/outputs")
        roadmap = generator.generate_roadmap("test_user", "Data Engineer", ["Python"])
        self.assertEqual(roadmap['target_role'], "Data Engineer")
        self.assertTrue(len(roadmap['modules']) > 0)
        self.assertTrue(os.path.exists("tests/outputs/test_user.json"))
        
    def test_clustering_mock_data(self):
        clustering = ProfileClustering()
        students = clustering.generate_mock_students(10)
        self.assertEqual(len(students), 10)
        self.assertIn('cgpa', students[0])
        self.assertIn('skills', students[0])

if __name__ == '__main__':
    unittest.main()
