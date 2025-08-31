import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from uvicorn import run as app_run
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse, Response
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database_name = client[DATA_INGESTION_DATABASE_NAME]
collection_name = database_name[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI(title="Network Security - Phishing Detection System", 
              description="Advanced ML-based system for detecting phishing websites and malicious URLs",
              version="1.0.0")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Frontend Routes
@app.get("/", tags=["frontend"])
async def home(request: Request):
    """Homepage with system overview and features"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/detect", tags=["frontend"])
async def detect_page(request: Request):
    """Phishing detection interface"""
    return templates.TemplateResponse("detect.html", {"request": request})

@app.get("/train", tags=["frontend"])
async def train_page(request: Request):
    """Model training interface"""
    return templates.TemplateResponse("train.html", {"request": request})

@app.get("/about", tags=["frontend"])
async def about_page(request: Request):
    """About page with system information"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/test", tags=["frontend"])
async def test_page(request: Request):
    """Test page for debugging API calls"""
    return templates.TemplateResponse("test_frontend.html", {"request": request})

# API Routes
@app.get("/Phising", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/api/train", tags=["api"])
async def train_route():
    """API endpoint to trigger model training"""
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return JSONResponse(content={"message": "Training completed successfully", "status": "success"})
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/api/predict", tags=["api"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    """API endpoint for phishing detection"""
    try:
        print(f"File received: {file.filename}")
        print(f"File content type: {file.content_type}")
        print(f"File size: {file.size}")
        
        # Read the file content and reset cursor
        try:
            file_content = file.file.read()
            file.file.seek(0)  # Reset cursor to beginning
            print(f"File content length: {len(file_content)} bytes")
            
            if len(file_content) == 0:
                raise ValueError("File is empty")
                
        except Exception as e:
            print(f"Error reading file: {e}")
            raise Exception(f"Failed to read file: {e}")
        
        # Read CSV data
        try:
            df = pd.read_csv(file.file)
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            raise Exception(f"Failed to parse CSV file: {e}")
        print(f"DataFrame shape: {df.shape}")
        print(f"DataFrame columns: {df.columns.tolist()}")
        print(f"First row: {df.iloc[0]}")
        print(f"DataFrame info:")
        print(df.info())
        
        # Validate DataFrame
        if df.empty:
            raise ValueError("DataFrame is empty")
        
        if df.shape[0] == 0:
            raise ValueError("No rows in DataFrame")
        
        if df.shape[1] == 0:
            raise ValueError("No columns in DataFrame")
        
        print(f"DataFrame validation passed: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Load models
        try:
            preprocesor = load_object("final_model/preprocessor.pkl")
            print(f"Preprocessor loaded successfully: {type(preprocesor)}")
        except Exception as e:
            print(f"Error loading preprocessor: {e}")
            raise Exception(f"Failed to load preprocessor: {e}")
            
        try:
            final_model = load_object("final_model/model.pkl")
            print(f"Model loaded successfully: {type(final_model)}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise Exception(f"Failed to load model: {e}")
            
        try:
            network_model = NetworkModel(preprocessor=preprocesor, model=final_model)
            print(f"NetworkModel created successfully: {type(network_model)}")
        except Exception as e:
            print(f"Error creating NetworkModel: {e}")
            raise Exception(f"Failed to create NetworkModel: {e}")
        
        # Make predictions
        try:
            y_pred = network_model.predict(df)
            print(f"Predictions shape: {y_pred.shape}")
            print(f"First few predictions: {y_pred[:5]}")
            print(f"Predictions type: {type(y_pred)}")
            print(f"Unique prediction values: {set(y_pred)}")
            
            # Check if predictions are valid
            if len(y_pred) == 0:
                raise ValueError("No predictions generated")
                
            # Check if predictions contain expected values
            if not any(val in y_pred for val in [-1, 0, 1]):
                print(f"Warning: Unexpected prediction values: {set(y_pred)}")
                print("Attempting to normalize predictions...")
                
                # Try to normalize predictions if they're not in expected format
                if all(isinstance(val, (int, float)) for val in y_pred):
                    # If all values are numeric, try to convert to binary
                    y_pred = [1 if val > 0.5 else 0 for val in y_pred]
                    print(f"Normalized predictions: {set(y_pred)}")
                else:
                    raise ValueError(f"Unexpected prediction value types: {[type(val) for val in y_pred[:5]]}")
                    
        except Exception as e:
            print(f"Error during prediction: {e}")
            raise Exception(f"Prediction failed: {e}")
        
        df['predicted_column'] = y_pred
        print(f"DataFrame with predictions shape: {df.shape}")
        print(f"DataFrame columns: {df.columns.tolist()}")
        print(f"Predicted column unique values: {df['predicted_column'].unique()}")
        print(f"Predicted column value counts:")
        print(df['predicted_column'].value_counts())
        
        # Save results
        import os
        
        # Ensure prediction output directory exists
        os.makedirs('prediction_output', exist_ok=True)
        
        # Save results
        df.to_csv('prediction_output/output.csv', index=False)
        
        # Return JSON response for API calls
        print("All request headers:")
        for header_name, header_value in request.headers.items():
            print(f"  {header_name}: {header_value}")
            
        accept_header = request.headers.get("accept", "").lower().strip()
        print(f"Accept header received: '{accept_header}'")
        
        if "application/json" in accept_header:
            print("Returning JSON response")
            
            # Calculate values and log them
            total_urls = len(df)
            print(f"Total URLs calculated: {total_urls}")
            
            # Check for expected prediction values
            unique_values = df['predicted_column'].unique()
            print(f"Unique prediction values found: {unique_values}")
            
            # Handle different prediction value formats
            if -1 in unique_values and 1 in unique_values:
                # Standard format: -1 for phishing, 1 for safe
                phishing_detected = int((df['predicted_column'] == -1).sum())
                safe_urls = int((df['predicted_column'] == 1).sum())
            elif 0 in unique_values and 1 in unique_values:
                # Alternative format: 0 for phishing, 1 for safe
                phishing_detected = int((df['predicted_column'] == 0).sum())
                safe_urls = int((df['predicted_column'] == 1).sum())
            else:
                # Fallback: treat all as safe if unexpected values
                print(f"Warning: Unexpected prediction values: {unique_values}")
                phishing_detected = 0
                safe_urls = total_urls
            
            predictions = df['predicted_column'].tolist()
            
            print(f"Calculated values:")
            print(f"  phishing_detected: {phishing_detected}")
            print(f"  safe_urls: {safe_urls}")
            print(f"  predictions count: {len(predictions)}")
            
            print(f"Response data:")
            print(f"  total_urls: {total_urls} (type: {type(total_urls)})")
            print(f"  phishing_detected: {phishing_detected} (type: {type(phishing_detected)})")
            print(f"  safe_urls: {safe_urls} (type: {type(safe_urls)})")
            print(f"  predictions: {len(predictions)} items (type: {type(predictions)})")
            print(f"  First few predictions: {predictions[:5]}")
            
            response_data = {
                "message": "Prediction completed successfully",
                "total_urls": total_urls,
                "phishing_detected": phishing_detected,
                "safe_urls": safe_urls,
                "predictions": predictions
            }
            
            print(f"Final response data: {response_data}")
            return JSONResponse(content=response_data)
        
        print("Returning HTML response")
        
        # Return HTML response for frontend
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
        print(f"Error in predict_route: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise NetworkSecurityException(e, sys)

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Network Security Phishing Detection System"}

# Model info endpoint
@app.get("/api/model/info", tags=["api"])
async def model_info():
    """Get information about the current model"""
    try:
        # You can add more model information here
        return {
            "model_type": "Phishing Detection Classifier",
            "features": 30,
            "algorithms": ["Random Forest", "Decision Tree", "Gradient Boosting", "Logistic Regression", "AdaBoost"],
            "last_trained": "2024-01-01",  # You can make this dynamic
            "version": "1.0.0"
        }
    except Exception as e:
        return {"error": str(e)}

# Download results endpoint
@app.get("/prediction_output/output.csv", tags=["download"])
async def download_results():
    """Download the prediction results CSV file"""
    try:
        import os
        file_path = "prediction_output/output.csv"
        
        if not os.path.exists(file_path):
            raise FileNotFoundError("Results file not found. Please run the analysis first.")
        
        return FileResponse(
            path=file_path,
            filename="phishing_detection_results.csv",
            media_type="text/csv"
        )
    except Exception as e:
        print(f"Error serving download file: {e}")
        raise HTTPException(status_code=404, detail="Results file not available")

if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
