# Network Security - Phishing Detection System

A comprehensive machine learning-based system for detecting phishing websites and malicious URLs using advanced ML algorithms and a robust training pipeline.

🌐 **Hosted Live at:** [http://51.20.189.64:8000/](http://51.20.189.64:8000/) (AWS EC2 Instance)

---

## 🚀 Features

* **Phishing Detection**: Advanced ML models to identify malicious websites and URLs
* **Multiple ML Algorithms**: Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, and AdaBoost
* **Automated Training Pipeline**: End-to-end ML pipeline with ingestion, validation, transformation, and training
* **RESTful API**: FastAPI-based web service for real-time predictions
* **MLflow Integration**: Experiment tracking and model versioning
* **MongoDB Integration**: Data storage and retrieval
* **Docker Support**: Containerized deployment ready
* **AWS EC2 Hosting**: Deployed and running live on an EC2 instance

---

## 🏗️ Architecture

```
networksecurity/
├── components/           # Core ML pipeline components
│   ├── data_ingestion.py
│   ├── data_validation.py
│   ├── data_transformation.py
│   └── model_trainer.py
├── entity/              # Data and configuration entities
├── pipeline/            # Training and prediction pipelines
├── utils/               # Utility functions and ML helpers
├── constants/           # Configuration constants
├── logging/             # Logging configuration
└── exception/           # Custom exception handling
```

---

## 📊 Dataset Features

The system analyzes 30+ features including:

* **URL Characteristics**: URL length, IP address presence, subdomain analysis
* **Security Indicators**: SSL state, HTTPS tokens, domain registration length
* **Behavioral Patterns**: Redirects, pop-ups, iframe usage, mouseover events
* **Reputation Metrics**: PageRank, Google indexing, web traffic analysis
* **Technical Indicators**: Port usage, DNS records, statistical reports

---

## 🛠️ Installation

### Prerequisites

* Python 3.8+
* MongoDB
* MLflow (optional for experiment tracking)
* Docker (optional for containerized deployment)

### Setup

```bash
# Clone the repository
git clone https://github.com/krishmaniyar/Phishing-Detection-System
cd Phishing-Detection-System

# Create and activate virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add environment variables in .env
MONGO_DB_URL=your_mongodb_connection_string
MLFLOW_TRACKING_URI=your_mlflow_uri (optional)
```

---

## 🚀 Usage

### 1. Access Online (Hosted)

The project is deployed on **AWS EC2** and accessible here:
👉 [http://51.20.189.64:8000/](http://51.20.189.64:8000/)

* **Swagger UI (Docs):** [http://51.20.189.64:8000/docs](http://51.20.189.64:8000/)
* **Train Endpoint:** [http://51.20.189.64:8000/train](http://51.20.189.64:8000/train)
* **Predict Endpoint:** [http://51.20.189.64:8000/predict](http://51.20.189.64:8000/predict)

### 2. Run Locally

```bash
# Start training pipeline
python app.py

# Trigger training
curl -X GET "http://localhost:8000/train"

# Make predictions (upload CSV)
curl -X POST "http://localhost:8000/predict" \
     -F "file=@your_data.csv"
```

---

## 🌐 API Endpoints

| Endpoint   | Method | Description                                |
| ---------- | ------ | ------------------------------------------ |
| `/Phising` | GET    | Redirects to API documentation             |
| `/train`   | GET    | Initiates model training pipeline          |
| `/predict` | POST   | Upload CSV file for phishing detection     |
| `/docs`    | GET    | Interactive API documentation (Swagger UI) |

👉 **Live Base URL:** `http://51.20.189.64:8000`

---

## 🐳 Docker Deployment

```bash
# Build the Docker image
docker build -t network-security .

# Run container
docker run -p 8000:8000 network-security
```

---

## ☁️ AWS EC2 Deployment Guide

1. **Launch EC2 Instance**

   * Choose **Ubuntu 20.04 LTS**
   * Open security group inbound rules: `8000`, `22` (SSH), `27017` (MongoDB if external)

2. **Install Dependencies**

   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip python3-venv git -y
   ```

3. **Clone Project & Setup**

   ```bash
   git clone https://github.com/krishmaniyar/Phishing-Detection-System
   cd Phishing-Detection-System
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run with Uvicorn**

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

5. **Keep Running in Background** (using `screen` or `tmux`)

   ```bash
   screen -S phishing
   uvicorn app:app --host 0.0.0.0 --port 8000
   # press Ctrl+A+D to detach
   ```

6. **Access the App**
   Visit: [http://your-ec2-public-ip:8000](http://your-ec2-public-ip:8000)

---

## 📈 Model Performance

* **Evaluation Metrics:** F1 Score, Precision, Recall, Accuracy
* **Automatic Model Selection:** Best performing algorithm chosen

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m "Added new feature"`)
4. Push branch (`git push origin feature/new-feature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Krish Maniyar**
📧 Email: [krishmaniyar27@gmail.com](mailto:krishmaniyar27@gmail.com)
💻 GitHub: [krishmaniyar](https://github.com/krishmaniyar)

---

## 🙏 Acknowledgments

* **MLflow** for experiment tracking
* **FastAPI** for API framework
* **Scikit-learn** for ML models
* **MongoDB** for database integration
* **AWS EC2** for cloud hosting

---

## 📞 Support

For support/questions:

* Open an issue in GitHub repo
* Email: [krishmaniyar27@gmail.com](mailto:krishmaniyar27@gmail.com)

---

⚠️ **Disclaimer:** This system is for **educational & research purposes**. Validate results before production use and follow best security practices.