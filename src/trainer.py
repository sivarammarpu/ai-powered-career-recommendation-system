import os
import json
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
import logging
import random
from src.clustering import ProfileClustering

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ModelTrainer")

class ModelTrainer:
    def __init__(self, models_dir: str = "models", reports_dir: str = "reports"):
        self.models_dir = models_dir
        self.reports_dir = reports_dir
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        self.mlb = MultiLabelBinarizer()
        
    def load_role_skill_matrix(self):
        path = os.path.join(self.models_dir, "role_skill_matrix.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Role-Skill Matrix not found at {path}. Run SkillRoleMapper first.")
        return pd.read_csv(path)

    def label_students(self, students: list, role_skill_df: pd.DataFrame):
        """
        Assigns a target role to each student based on their skills and the matrix.
        """
        logger.info("Labeling synthetic students...")
        labeled_data = []
        
        # Create a lookup: skill -> {role: score}
        skill_role_map = {}
        for _, row in role_skill_df.iterrows():
            skill = row['skill']
            role = row['role']
            score = row['p_skill_given_role'] # or use raw count
            if skill not in skill_role_map: skill_role_map[skill] = {}
            skill_role_map[skill][role] = score
            
        for student in students:
            scores = {}
            for skill in student['skills']:
                if skill in skill_role_map:
                    for role, score in skill_role_map[skill].items():
                        scores[role] = scores.get(role, 0) + score
            
            if not scores:
                target_role = "Generalist" # Fallback
            else:
                target_role = max(scores, key=scores.get)
                
            student['target_role'] = target_role
            labeled_data.append(student)
            
        return labeled_data

    def train(self):
        # 1. Generate Data
        clustering = ProfileClustering()
        students = clustering.generate_mock_students(500)
        
        # 2. Label Data
        try:
            role_skill_df = self.load_role_skill_matrix()
            labeled_students = self.label_students(students, role_skill_df)
        except FileNotFoundError:
            logger.warning("Role-Skill Matrix not found. Using mock labeling for bootstrapping.")
            # Mock labeling if matrix doesn't exist yet (for first run/testing)
            labeled_students = students
            roles = ["Data Engineer", "Data Scientist", "Backend Engineer", "Frontend Engineer", "DevOps Engineer"]
            for s in labeled_students:
                s['target_role'] = random.choice(roles)

        # 3. Prepare Features
        df = pd.DataFrame(labeled_students)
        X_skills = self.mlb.fit_transform(df['skills'])
        # We could add CGPA, Interests etc. For now, just skills.
        X = X_skills
        y = df['target_role']
        
        # 4. Train Test Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 5. Train Model
        logger.info("Training RandomForest Classifier...")
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        
        # 6. Evaluate
        y_pred = clf.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        logger.info("Model Evaluation:\n" + classification_report(y_test, y_pred))
        
        # 7. Save Artifacts
        with open(os.path.join(self.reports_dir, "metrics.json"), 'w') as f:
            json.dump(report, f, indent=2)
            
        with open(os.path.join(self.models_dir, "best_model.pkl"), 'wb') as f:
            pickle.dump({
                "model": clf,
                "mlb": self.mlb,
                "classes": clf.classes_
            }, f)
            
        logger.info(f"Saved model to {os.path.join(self.models_dir, 'best_model.pkl')}")

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train()
