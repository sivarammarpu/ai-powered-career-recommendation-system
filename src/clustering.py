import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProfileClustering")

class ProfileClustering:
    def __init__(self, output_dir: str = "models"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.mlb = MultiLabelBinarizer()
        self.scaler = StandardScaler()
        self.kmeans = None

    def generate_mock_students(self, count: int = 100):
        logger.info(f"Generating {count} mock student profiles...")
        students = []
        skills_pool = ["python", "java", "sql", "react", "aws", "docker", "pandas", "pytorch", "node.js"]
        interests_pool = ["Data Science", "Web Development", "DevOps", "Cloud Computing"]
        
        for i in range(count):
            students.append({
                "id": f"student_{i}",
                "cgpa": round(random.uniform(6.0, 10.0), 2),
                "skills": random.sample(skills_pool, k=random.randint(2, 6)),
                "interests": random.sample(interests_pool, k=random.randint(1, 2)),
                "internships": random.randint(0, 2)
            })
        return students

    def train_clusters(self, students: list, n_clusters: int = 4):
        logger.info("Preparing data for clustering...")
        
        # Features: CGPA (scaled), Skills (one-hot)
        df = pd.DataFrame(students)
        
        # 1. Encode Skills
        skills_encoded = self.mlb.fit_transform(df['skills'])
        skills_df = pd.DataFrame(skills_encoded, columns=self.mlb.classes_)
        
        # 2. Scale CGPA
        cgpa_scaled = self.scaler.fit_transform(df[['cgpa']])
        
        # 3. Combine
        X = np.hstack([cgpa_scaled, skills_encoded])
        
        # 4. KMeans
        logger.info(f"Training KMeans with k={n_clusters}...")
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.kmeans.fit(X)
        
        # 5. Analyze Clusters
        df['cluster'] = self.kmeans.labels_
        logger.info("Cluster centers (CGPA part):")
        logger.info(self.kmeans.cluster_centers_[:, 0]) # Just CGPA for quick check
        
        # Save models
        model_path = os.path.join(self.output_dir, "kmeans_cluster_model.pkl")
        with open(model_path, 'wb') as f:
            pickle.dump({
                "kmeans": self.kmeans,
                "mlb": self.mlb,
                "scaler": self.scaler,
                "feature_names": ["cgpa"] + list(self.mlb.classes_)
            }, f)
            
        logger.info(f"Saved clustering model to {model_path}")
        
        # Save cluster report
        report_path = os.path.join("reports", "cluster_analysis.md")
        with open(report_path, 'w') as f:
            f.write(f"# Cluster Analysis\n\n")
            f.write(f"Number of clusters: {n_clusters}\n\n")
            for i in range(n_clusters):
                cluster_students = df[df['cluster'] == i]
                avg_cgpa = cluster_students['cgpa'].mean()
                common_skills = pd.Series([s for sublist in cluster_students['skills'] for s in sublist]).value_counts().head(3).index.tolist()
                f.write(f"## Cluster {i}\n")
                f.write(f"- Size: {len(cluster_students)}\n")
                f.write(f"- Avg CGPA: {avg_cgpa:.2f}\n")
                f.write(f"- Top Skills: {', '.join(common_skills)}\n\n")
                
        logger.info(f"Saved cluster report to {report_path}")

if __name__ == "__main__":
    clustering = ProfileClustering()
    students = clustering.generate_mock_students(200)
    clustering.train_clusters(students)
