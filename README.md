# AI-Powered Career Recommendation System

> **Owned and Developed by [Sivarammarpu](https://github.com/sivarammarpu)**

An end-to-end AI system that recommends career roles and generates personalized learning roadmaps based on student profiles (CGPA, skills, interests, internships).

## 🎯 Features
- **Job Data Collection**: Mock job scraper generating realistic job descriptions across 5 tech roles
- **NLP Skill Extraction**: Regex-based skill extraction from job descriptions
- **Skill-Role Mapping**: Probabilistic mapping of skills to career roles
- **Profile Clustering**: KMeans clustering to identify student archetypes
- **ML Role Prediction**: RandomForest classifier predicting suitable roles with confidence scores
- **Learning Roadmap Generator**: Personalized 12-week learning paths with curated resources
- **Interactive UI**: Streamlit-based web interface with PDF export

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sivarammarpu/ai-powered-career-recommendation-system.git
   cd ai-powered-career-recommendation-system
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the data pipeline**:
   ```bash
   python run_pipeline.py
   ```

5. **Launch the UI**:
   ```bash
  [ streamlit run ui/app.py](https://career-ai-system.streamlit.app/)
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure
```
ai-powered-career-recommendation-system/
├── data/
│   ├── jobs/raw/          # Raw job descriptions (100 mock jobs)
│   ├── jobs/parsed/       # Parsed and enriched job data
│   ├── skills/            # Skill dictionary and mappings
│   └── embeddings/        # TF-IDF vectors
├── models/
│   ├── best_model.pkl     # Trained RandomForest classifier
│   ├── role_skill_matrix.csv
│   └── kmeans_cluster_model.pkl
├── src/
│   ├── data_collector.py  # Job data generation
│   ├── parser_nlp.py      # Skill extraction
│   ├── skill_mapper.py    # Skill-role mapping
│   ├── clustering.py      # Student clustering
│   ├── trainer.py         # Model training
│   └── roadmap.py         # Roadmap generation
├── ui/
│   └── app.py             # Streamlit UI
├── tests/
│   └── test_agents.py     # Unit tests
├── deploy/
│   ├── Dockerfile
│   └── docker-compose.yml
├── run_pipeline.py        # End-to-end pipeline
└── README.md
```

## 🎓 How It Works

1. **Data Collection**: Generates 100 mock job descriptions across 5 roles (Data Engineer, Data Scientist, Backend Engineer, Frontend Engineer, DevOps Engineer)
2. **Skill Extraction**: Extracts technical skills from job descriptions using regex patterns
3. **Role Mapping**: Computes P(skill|role) probabilities to map skills to roles
4. **Clustering**: Groups student profiles into archetypes using KMeans
5. **Model Training**: Trains a RandomForest classifier on 500 synthetic student profiles
6. **Prediction**: Predicts top-3 suitable roles with confidence scores
7. **Roadmap**: Generates personalized 12-week learning plans based on skill gaps

## 🧪 Testing

Run unit tests:
```bash
python tests/test_agents.py
```

## 🐳 Docker Deployment

```bash
cd deploy
docker-compose up
```

## 📊 Sample Output

For a student with:
- CGPA: 8.1
- Skills: Python, SQL, Pandas, Git
- Interests: Data Engineering, Backend

**Recommendations**:
1. **Data Engineer** (78% match) - Strong SQL+Python+ETL signals
2. **Backend Engineer** (55% match) - Git + internship experience
3. **DevOps Engineer** (35% match) - AWS cert needed

**12-Week Roadmap**: Advanced SQL → ETL with Airflow → Capstone Project

## 🛠️ Tech Stack
- **ML/AI**: scikit-learn, XGBoost, pandas, numpy
- **NLP**: Regex-based extraction (expandable to spaCy)
- **UI**: Streamlit
- **Visualization**: Matplotlib, Seaborn, Plotly
- **PDF Generation**: FPDF
- **Deployment**: Docker, Docker Compose

## 📈 Future Enhancements
- [ ] Real job scraping from Indeed/Naukri APIs
- [ ] SHAP-based model explainability
- [ ] Advanced NLP with spaCy EntityRuler
- [ ] User authentication and profile persistence
- [ ] Cloud deployment (GCP/AWS)
- [ ] Resume parsing from PDF/DOCX
- [ ] Integration with LinkedIn API

## 👤 Author

**Sivarammarpu**
- GitHub: [@sivarammarpu](https://github.com/sivarammarpu)

## 📝 License

This project is owned and developed by Sivarammarpu.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## ⭐ Show your support

Give a ⭐️ if this project helped you!

