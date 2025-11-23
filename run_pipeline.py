import os
import subprocess
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Pipeline")

def run_module(module_name, step_name):
    logger.info(f"Starting {step_name}...")
    try:
        # Run as module: python -m src.module_name
        result = subprocess.run(
            [sys.executable, "-m", module_name], 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=os.getcwd() # Ensure CWD is project root
        )
        logger.info(f"{step_name} completed successfully.")
        logger.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"{step_name} failed with error:\n{e.stderr}")
        logger.error(f"Stdout:\n{e.stdout}")
        sys.exit(1)

def main():
    logger.info("Starting End-to-End Pipeline...")
    
    # 1. Data Collection
    if not os.path.exists("data/jobs/raw"):
        run_module("src.data_collector", "Data Collection")
    else:
        logger.info("Data Collection skipped (raw data exists).")

    # 2. Parsing & NLP
    run_module("src.parser_nlp", "Parsing & NLP")
    
    # 3. Skill-Role Mapping
    run_module("src.skill_mapper", "Skill-Role Mapping")
    
    # 4. Profile Clustering
    run_module("src.clustering", "Profile Clustering")
    
    # 5. Model Training
    run_module("src.trainer", "Model Training")
    
    logger.info("Pipeline finished successfully! You can now run the UI.")
    logger.info("Run: streamlit run ui/app.py")

if __name__ == "__main__":
    main()
