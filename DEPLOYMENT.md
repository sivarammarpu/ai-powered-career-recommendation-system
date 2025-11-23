# AI-Powered Career Recommendation System
# Streamlit Cloud Deployment Configuration

This file ensures the app runs correctly on Streamlit Cloud.

## Deployment Steps

1. Go to: https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - Repository: sivarammarpu/ai-powered-career-recommendation-system
   - Branch: main
   - Main file path: ui/app.py
5. Click "Deploy"

## Important Notes

- The app will automatically run `run_pipeline.py` on first deployment to generate models
- All dependencies will be installed from requirements.txt
- The .streamlit/config.toml will configure the app settings
