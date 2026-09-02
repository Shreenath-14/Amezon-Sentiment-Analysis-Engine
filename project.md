# Project Overview: Amazon Review Sentiment Analyzer

## 1. Project Goal
Rebuild a diploma-level sentiment analysis web application for Amazon product reviews, focusing on code quality, developer proficiency, and a clean, unembellished user experience.

## 2. Architecture & Tech Stack
**Frontend:**
- Framework: Next.js (React-based, optimized for performance)
- Styling: Bootstrap CSS (Consider React-Bootstrap for component compatibility) / HTML
- Animation: Framer Motion (Lightweight interactions)

**Backend:**
- Framework: Python 3.12 with Flask
- Web Scraping: (To be decided - e.g., BeautifulSoup, Playwright, or Selenium)
- NLP/Sentiment Analysis: (To be decided - e.g., NLTK, VADER, TextBlob, or Hugging Face Transformers)

**Database:**
- MySQL (Relational storage for products, scraped reviews, and computed sentiment scores)

## 3. Core Features
- **URL Input:** User provides an Amazon product URL.
- **Scraping Engine:** Extracts recent/top product reviews from the provided URL.
- **NLP Processing:** Analyzes review text and categorizes sentiment.
- **Scoring System:** Aggregates sentiment into a scale: Worst, Good, Better, Best.
- **Dashboard/Results:** Displays the final score and a breakdown of the reviews.

## 4. Development Phases
### Phase 1: Planning & Database Design
- Define the database schema in MySQL (Tables for Products, Reviews, Scores).
- Set up the local MySQL environment.

### Phase 2: The Web Scraper (Python/Flask context)
- Formulate the scraping logic to bypass basic bot protections.
- Extract reviewer text, rating, and date.
- Store raw data into the MySQL database.

### Phase 3: NLP & Sentiment Logic (Python)
- Clean and preprocess the scraped text (remove stop words, punctuation, etc.).
- Apply the chosen NLP model to calculate polarity.
- Map the raw scores to the custom scale (Worst -> Best).

### Phase 4: Backend API (Flask)
- Create REST endpoints to receive the URL from the frontend.
- Orchestrate the scraping and NLP functions.
- Return the structured JSON response to the frontend.

### Phase 5: Frontend Development (Next.js)
- Build the UI layout using Bootstrap.
- Integrate Framer Motion for loading states (since scraping and NLP take time).
- Connect to the Flask API.

### Phase 6: Refinement & Optimization
- Handle edge cases (e.g., invalid URLs, Amazon captchas).
- Optimize Next.js rendering and Flask response times.