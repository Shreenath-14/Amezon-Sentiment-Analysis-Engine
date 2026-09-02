# Amazon Sentiment Engine

A full-stack, end-to-end artificial intelligence pipeline that extracts live Amazon product reviews, analyzes their emotional context using a Hugging Face transformer model, and visualizes the aggregate metrics on a modern web dashboard.

## Overview

Traditional e-commerce sentiment analysis often relies on static, pre-downloaded CSV files. This project bridges the gap between Data Engineering and Machine Learning by building a live ETL (Extract, Transform, Load) pipeline. It empowers users to input any standard Amazon product URL, instantly scrape the most recent customer feedback, perform NLP inference to determine sentiment confidence scores, and persist the normalized data into a relational database for historical tracking.

## Features

* **Live Web Scraping:** Dynamically extracts customer reviews and product URLs directly from Amazon bypassing basic bot-detections using authenticated session headers.
* **State-of-the-Art NLP:** Utilizes a pre-trained DistilBERT transformer (Default) for highly accurate, contextual sentiment classification (Positive/Negative) and confidence scoring.
* **Relational Persistence:** Robust MySQL database schema designed to handle varying string lengths and enforce relational mapping between products and individual reviews.
* **Executive Dashboard:** A responsive Next.js and Bootstrap frontend featuring KPI cards, dynamic progress bars, and granular review breakdowns.
* **Secure Configuration:** Environment variable management to protect database credentials and session tokens.

## Architecture & Model

* **Model Architecture:** Transformer (DistilBERT)
* **Base Model:** `distilbert-base-uncased-finetuned-sst-2-english` (Hugging Face)
* **Inference Approach:** Zero-shot application of a fine-tuned sentiment analysis pipeline. The backend passes scraped textual data directly to the model to retrieve polarity labels and floating-point confidence arrays.

```text
                    ┌────────────────────────────┐
                    │  Next.js Client UI         │
                    └─────────────┬──────────────┘
                                  │ POST /api/analyze-reviews
                    ┌─────────────↓──────────────┐
                    │  Flask REST API (Backend)  │
                    └─────────────┬──────────────┘
                                  │
          ┌───────────────────────┴──────────────────────┐
          ↓                                              ↓
 ┌──────────────────┐                           ┌──────────────────┐
 │  BeautifulSoup4  │ ───(Raw Text Array)───>   │  DistilBERT NLP  │
 │  (Amazon Scraper)│                           │  (Hugging Face)  │
 └──────────────────┘                           └────────┬─────────┘
                                                         │
                                                ┌────────↓─────────┐
                                                │ MySQL Database   │
                                                │ (Relational DB)  │
                                                └──────────────────┘

```

## Dataset

Unlike traditional ML repositories, this project does not rely on a static dataset.

* **Source:** Real-time DOM extraction from `amazon.in` via standard HTTP requests.
* **Format:** Unstructured HTML parsed into clean Python arrays containing raw text reviews.
* **Preprocessing:** Removal of HTML tags, whitespace stripping, and URL parameter truncation using RegEx to isolate the core ASIN (Amazon Standard Identification Number).

## Installation

### Prerequisites

* Python 3.12+
* Node.js (v18+)
* MySQL Server & Workbench

### 1. Database Setup

Execute the following SQL commands in your MySQL instance to create the required schema:

```sql
CREATE DATABASE amazon_sentiment;
USE amazon_sentiment;

CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    amazon_url TEXT,
    product_name VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    review_text TEXT,
    sentiment_score FLOAT,
    sentiment_label VARCHAR(50),
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

```

### 2. Backend Setup

```bash
# Clone the repository
git clone <repository_url>
cd Sentiment-Analysis/backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install Python dependencies
pip install flask flask-cors requests beautifulsoup4 transformers torch mysql-connector-python python-dotenv

```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
npm install bootstrap bootstrap-icons

```

## Configuration

Create a `.env` file in the root of the `backend` directory to store your sensitive credentials safely:

```env
MYSQL_PASSWORD='your_local_mysql_password'
AMAZON_COOKIE='session-id=... (Extract from Chrome Network Tab)'

```

## Usage

1. **Start the Flask AI Engine:**

```bash
cd backend
python app.py

```

2. **Start the Next.js Dashboard:**

```bash
cd frontend
npm run dev

```

3. Open `http://localhost:3000` in your browser.
4. Paste a valid Amazon product URL and click **Analyze**.

## Project Structure

```text
Sentiment Analysis/
├── backend/
│   ├── app.py                # Flask server routing and CORS handling
│   ├── db_manager.py         # MySQL connection and insertion logic
│   ├── nlp_engine.py         # Hugging Face DistilBERT initialization
│   ├── scraper.py            # BeautifulSoup DOM parsing and ASIN regex
│   ├── .env                  # Hidden credentials
│   └── venv/                 # Python environment
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.js       # Main React/Bootstrap dashboard component
│   │       └── globals.css   # Global styling overrides
│   ├── package.json
│   └── next.config.mjs
└── README.md

```

## Limitations

* **Session Expiration:** The current scraping architecture relies on authenticated session cookies. If the cookie expires, Amazon will serve a CAPTCHA or Sign-In page, requiring manual `.env` updates.
* **Hardware Dependency:** Inference is run locally via the CPU. Extremely high volumes of text may cause temporary bottlenecks depending on the host machine's processing power.

## Future Work

* **Historical Query Endpoint:** Implementing a `GET /api/history` route to fetch and visualize past product analyses directly from MySQL without re-scraping.
* **Proxy Rotation:** Integrating commercial scraping APIs (e.g., Bright Data) to automatically bypass bot detection and CAPTCHAs for production-scale resilience.
* **Containerization:** Wrapping the Next.js frontend, Flask backend, and MySQL database into a unified `docker-compose.yml` file for immediate deployment.

## Authors

**Shreenath**

* Focus: AI Engineering, Backend Development, & Data Analysis.