# Network Security - Phishing Detection System

A comprehensive machine learning-based system for detecting phishing websites and malicious URLs using advanced ML algorithms and a robust training pipeline.

## 🚀 Features

- **Phishing Detection**: Advanced ML models to identify malicious websites and URLs
- **Multiple ML Algorithms**: Support for Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, and AdaBoost
- **Automated Training Pipeline**: End-to-end ML pipeline with data ingestion, validation, transformation, and model training
- **RESTful API**: FastAPI-based web service for real-time predictions
- **MLflow Integration**: Experiment tracking and model versioning
- **MongoDB Integration**: Data storage and retrieval capabilities
- **Docker Support**: Containerized deployment ready

## 🏗️ Architecture

The project follows a modular architecture with the following components:

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

## 📊 Dataset Features

The system analyzes 30+ features including:
- **URL Characteristics**: URL length, IP address presence, subdomain analysis
- **Security Indicators**: SSL state, HTTPS tokens, domain registration length
- **Behavioral Patterns**: Redirects, pop-ups, iframe usage, mouseover events
- **Reputation Metrics**: PageRank, Google indexing, web traffic analysis
- **Technical Indicators**: Port usage, DNS records, statistical reports

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB
- MLflow (optional for experiment tracking)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/krishmaniyar/Phishing-Detection-System
   cd Phishing-Detection-System
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file with:
   ```env
   MONGO_DB_URL=your_mongodb_connection_string
   MLFLOW_TRACKING_URI=your_mlflow_uri (optional)
   ```

## 🚀 Usage

### Training the Model

1. **Start the training pipeline**
   ```bash
   python app.py
   ```

2. **Trigger training via API**
   ```bash
   curl -X GET "http://localhost:8000/train"
   ```

### Making Predictions

1. **Start the prediction service**
   ```bash
   python app.py
   ```

2. **Upload CSV file for prediction**
   ```bash
   curl -X POST "http://localhost:8000/predict" \
        -F "file=@your_data.csv"
   ```

## 🌐 API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/Phising` | GET | Redirects to API documentation |
| `/train` | GET | Initiates model training pipeline |
| `/predict` | POST | Upload CSV file for phishing detection |
| `/docs` | GET | Interactive API documentation (Swagger UI) |

### Prediction Input Format

Upload a CSV file with the following columns (all features should be numerical):
- `having_IP_Address`
- `URL_Length`
- `Shortining_Service`
- `having_At_Symbol`
- `double_slash_redirecting`
- `Prefix_Suffix`
- `having_Sub_Domain`
- `SSLfinal_State`
- `Domain_registeration_length`
- `Favicon`
- `port`
- `HTTPS_token`
- `Request_URL`
- `URL_of_Anchor`
- `Links_in_tags`
- `SFH`
- `Submitting_to_email`
- `Abnormal_URL`
- `Redirect`
- `on_mouseover`
- `RightClick`
- `popUpWidnow`
- `Iframe`
- `age_of_domain`
- `DNSRecord`
- `web_traffic`
- `Page_Rank`
- `Google_Index`
- `Links_pointing_to_page`
- `Statistical_report`

## 🐳 Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t network-security .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 network-security
   ```

## 📁 Project Structure

```
Network-Security/
├── app.py                 # FastAPI application entry point
├── main.py               # Main execution script
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup configuration
├── Dockerfile           # Docker configuration
├── data_schema/         # Data validation schemas
├── final_model/         # Trained model artifacts
├── Network_Data/        # Training datasets
├── prediction_output/   # Prediction results
├── templates/           # HTML templates
├── networksecurity/     # Core package modules
└── notebooks/           # Jupyter notebooks
```

## 🔧 Configuration

### Training Pipeline Configuration
The system uses YAML-based configuration for:
- Data ingestion parameters
- Model training hyperparameters
- Validation rules
- Pipeline execution settings

### MLflow Configuration
- Experiment tracking
- Model versioning
- Performance metrics logging
- Model registry integration

## 📈 Model Performance

The system evaluates multiple ML algorithms and automatically selects the best performing model based on:
- F1 Score
- Precision
- Recall
- Overall accuracy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Krish Maniyar**
- Email: krishmaniyar27@gmail.com
- GitHub: [krishmaniyar](https://github.com/krishmaniyar)

## 🙏 Acknowledgments

- MLflow for experiment tracking
- FastAPI for the web framework
- Scikit-learn for machine learning algorithms
- MongoDB for data storage

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: krishmaniyar27@gmail.com

---

**Note**: This system is designed for educational and research purposes. Always validate results in production environments and follow security best practices.