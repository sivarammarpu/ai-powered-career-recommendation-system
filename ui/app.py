import streamlit as st
import pandas as pd
import pickle
import os
import sys
import json
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.roadmap import RoadmapGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UI")

st.set_page_config(page_title="AI Career Recommender", layout="wide")

@st.cache_resource
def load_model():
    model_path = "models/best_model.pkl"
    if not os.path.exists(model_path):
        return None
    with open(model_path, 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_skill_matrix():
    matrix_path = "models/role_skill_matrix.csv"
    if not os.path.exists(matrix_path):
        return None
    return pd.read_csv(matrix_path)

def main():
    st.title("AI-Powered Career Recommendation System")
    st.markdown("Enter your profile details to get personalized career advice and a learning roadmap.")

    with st.sidebar:
        st.header("Student Profile")
        cgpa = st.slider("CGPA (0-10)", 0.0, 10.0, 8.0)
        
        # Skills input
        all_skills = ["Python", "Java", "SQL", "React", "AWS", "Docker", "Pandas", "PyTorch", "Node.js", "Linux", "Git", "C++", "JavaScript", "HTML", "CSS"]
        skills = st.multiselect("Select your Skills", all_skills, default=["Python", "SQL"])
        
        interests = st.multiselect("Interests", ["Data Science", "Web Development", "DevOps", "Cloud Computing", "Backend", "Frontend"], default=["Data Science"])
        
        internships = st.number_input("Number of Internships", 0, 5, 1)
        
        if st.button("Get Recommendations"):
            if not skills:
                st.error("Please select at least one skill.")
            else:
                process_submission(cgpa, skills, interests, internships)

def process_submission(cgpa, skills, interests, internships):
    model_data = load_model()
    if not model_data:
        st.error("Model not trained yet. Please run the training pipeline.")
        return

    clf = model_data['model']
    mlb = model_data['mlb']
    
    # Prepare input
    # Note: The model was trained on just skills for now in trainer.py
    # If we added CGPA, we'd need to scale it here too.
    # For MVP, let's assume the model expects just One-Hot encoded skills.
    
    # Transform skills
    # Handle unknown skills gracefully
    # valid_skills = set(mlb.classes_)
    # filtered_skills = [s for s in skills if s in valid_skills]
    
    # MLB expects a list of lists (samples)
    X_input = mlb.transform([skills])
    
    # Predict
    probas = clf.predict_proba(X_input)[0]
    classes = clf.classes_
    
    # Get top 3
    top_indices = probas.argsort()[-3:][::-1]
    top_roles = [(classes[i], probas[i]) for i in top_indices]
    
    st.divider()
    st.header("Recommended Roles")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        best_role = top_roles[0][0]
        st.success(f"**Top Recommendation:** {best_role} ({top_roles[0][1]:.2%} match)")
        
        for role, score in top_roles[1:]:
            st.info(f"{role}: {score:.2%} match")
            
        # Explainability (Simple feature importance proxy: missing skills)
        st.subheader("Why this role?")
        role_skill_df = load_skill_matrix()
        if role_skill_df is not None:
            # Get top skills for the best role
            role_skills = role_skill_df[role_skill_df['role'] == best_role].sort_values('p_skill_given_role', ascending=False)['skill'].head(10).tolist()
            
            # Identify gaps
            # Normalize for comparison
            user_skills_lower = [s.lower() for s in skills]
            missing = [s for s in role_skills if s.lower() not in user_skills_lower]
            
            st.write(f"Key skills you have: {', '.join([s for s in skills if s.lower() in [rs.lower() for rs in role_skills]])}")
            st.write(f"Key skills to learn: {', '.join(missing)}")
            
            # Generate Roadmap
            st.subheader("Learning Roadmap")
            generator = RoadmapGenerator()
            roadmap = generator.generate_roadmap("current_user", best_role, missing)
            
            for module in roadmap['modules']:
                with st.expander(f"Week {module.get('week')}: {module['topic']}"):
                    if 'description' in module:
                        st.write(module['description'])
                    if 'resources' in module:
                        for res in module['resources']:
                            st.markdown(f"- [{res['title']}]({res['url']}) ({res['type']})")
                            
            # Download PDF
            pdf_path = f"outputs/roadmaps/{roadmap['student_id']}.pdf"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Roadmap PDF",
                        data=pdf_file,
                        file_name=f"roadmap_{best_role.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )

    with col2:
        st.subheader("Market Insights")
        st.write("Based on job market data:")
        # Placeholder for real stats
        st.metric("Average Salary", "$120k")
        st.metric("Job Openings", "15,000+")

if __name__ == "__main__":
    main()
