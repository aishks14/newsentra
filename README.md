# Newsentra – AI-Powered News Research & Analysis Platform

## Overview

Newsentra is an AI-powered news research and summarization platform that aggregates news articles from multiple trusted news providers, analyzes them using Large Language Models (LLMs), and generates structured summaries with key insights, highlights, sentiment analysis, and source references.

The platform is designed to provide users with a single interface for discovering, analyzing, summarizing, and exporting news from various domains including Politics, Business, Technology, Sports, Health, Science, Environment, Weather, and more.

---

# Key Features

## Multi-Source News Aggregation

Newsentra collects news from multiple news providers:

* NewsAPI
* GNews
* NewsData.io
* The Guardian

This ensures broader coverage and reduces dependency on a single source.

---

## AI-Powered Summarization

Uses Groq-hosted LLMs to generate:

* Key Highlights
* Detailed Summary
* Key Takeaways
* Important Notes

The summaries are generated only from retrieved news articles.

---

## Multi-Language Support

Users can:

* Search news in multiple languages
* Translate generated summaries
* Read news insights in their preferred language

---

## News Analytics Dashboard

Provides useful metrics including:

* Total Articles
* News Sources
* Countries Covered
* Sentiment Analysis
* Word Count
* Reading Time
* Estimated Tokens
* Response Time

---

## Source Breakdown

Displays contribution from each news provider:

* NewsAPI
* GNews
* NewsData.io
* The Guardian

This helps users understand source distribution.

---

## Smart Article Display

Each article includes:

* Title
* Source
* Publication Date
* Sentiment
* Description
* Featured Image
* Read Full Article Link

Articles are shown in expandable cards for improved readability.

---

## Export Capabilities

Generated summaries can be exported as:

* PDF
* TXT

Useful for research, presentations, reporting, and documentation.

---

# Technology Stack

## Frontend

* Streamlit

---

## Backend

* Python

---

## AI / LLM

* Groq API

Supported Models:

* llama-3.3-70b-versatile
* gemma2-9b-it
* llama-3.1-8b-instant
* deepseek-r1-distill-llama-70b
* deepseek-r1-distill-llama-13b

---

## News Sources

* NewsAPI
* GNews
* NewsData.io
* The Guardian

---

## NLP Libraries

* LangChain
* TextBlob

---

## Export Libraries

* FPDF

---

# Project Architecture

```text
Newsentra
│
├── app.py
│
├── config
│   └── categories.py
│   └── language_config.py
│   └── settings.py
│
├── news
│   ├── aggregator.py
│   ├── newsapi_client.py
│   ├── gnews_client.py
│   ├── newsdata_client.py
│   └── guardian_client.py
│
├── llm
│   ├── groq_client.py
│   ├── prompts.py
│   └── summarizer.py
│
├── export
│   ├── pdf_export.py
│   └── txt_export.py
│
├── utils
│   ├── helpers.py
│   ├── translator.py
│   ├── sentiment.py
│   └── analytics.py
│
├── fonts
│   └── DejaVuSans.ttf
│
├── assets
│
├── requirements.txt
│
└── README.md
```

---

# Module Description

## app.py

Main Streamlit application.

Responsibilities:

* User Interface
* Search Execution
* Session Management
* Analytics Display
* Summary Rendering
* Article Rendering
* Export Handling

---

## config/settings.py

Stores:

* API Keys
* Environment Variables
* Application Configuration

Examples:

* GROQ_API_KEY
* NEWS_API_KEY
* GNEWS_API_KEY
* NEWSDATA_API_KEY
* GUARDIAN_API_KEY

---

## news/

Contains all news source integrations.

### aggregator.py

Responsible for:

* Calling all news providers
* Merging results
* Deduplication
* Returning source statistics

### newsapi_client.py

Fetches news from NewsAPI.

### gnews_client.py

Fetches news from GNews.

### newsdata_client.py

Fetches news from NewsData.io.

### guardian_client.py

Fetches news from The Guardian API.

---

## llm/

Contains AI processing logic.

### groq_client.py

Initializes and returns Groq LLM instances.

### prompts.py

Contains prompt templates used for summary generation.

### summarizer.py

Responsible for:

* Formatting article content
* Calling LLM
* Generating structured summaries

---

## export/

### pdf_export.py

Creates PDF versions of generated summaries.

### txt_export.py

Creates TXT versions of generated summaries.

---

## utils/

### helpers.py

Utility functions:

* Relevance filtering
* Date filtering
* Data cleaning
* Deduplication support

### translator.py

Handles summary translation.

### sentiment.py

Calculates sentiment using TextBlob.

Possible values:

* Positive
* Neutral
* Negative

### analytics.py

Computes:

* Word Count
* Reading Time
* Token Estimation
* Source Statistics

---

# Search Workflow

## Step 1

User enters query.

Example:

```text
IPL 2026
```

---

## Step 2

Newsentra fetches articles from:

* NewsAPI
* GNews
* NewsData.io
* The Guardian

---

## Step 3

Results are:

* Combined
* Deduplicated
* Filtered

---

## Step 4

Relevant articles are passed to the LLM.

---

## Step 5

LLM generates:

* Key Highlights
* Detailed Summary
* Key Takeaways
* Important Notes

---

## Step 6

Analytics are calculated.

---

## Step 7

Results are displayed to the user.

---

# Summary Generation Flow

```text
User Query
     │
     ▼
News Sources
     │
     ▼
Aggregator
     │
     ▼
Filtered Articles
     │
     ▼
Groq LLM
     │
     ▼
Structured Summary
     │
     ▼
Translation
     │
     ▼
Analytics + Export
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-repository/newsentra.git

cd newsentra
```

---

## (Recommended) Create a Virtual Environment

Creating a virtual environment helps isolate project dependencies and avoid conflicts with globally installed packages.

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_key

NEWS_API_KEY=your_key

GNEWS_API_KEY=your_key

NEWSDATA_API_KEY=your_key

GUARDIAN_API_KEY=your_key
```

---

# Run Application

```bash
streamlit run app.py
```

Default URL:

```text
http://localhost:8501
```

---

# User Workflow

1. Open Newsentra.
2. Select Category.
3. Select Language.
4. Select Date Range.
5. Enter Search Query.
6. View AI Summary.
7. Analyze Statistics.
8. Read Source Articles.
9. Export Results.

---

# Current Capabilities

✔ Multi-source aggregation

✔ AI summarization

✔ Sentiment analysis

✔ Multi-language support

✔ Article images

✔ Source attribution

✔ Analytics dashboard

✔ PDF export

✔ TXT export

✔ Follow-up searches

✔ Responsive Streamlit interface

---

# Future Enhancements

* Real-time news streaming
* User authentication
* Saved searches
* Search history
* Topic comparison
* Trend analysis
* News timeline visualization
* Article clustering
* RAG-based research mode
* Citation generation
* PowerPoint export
* Email reports
* Dashboard personalization

---

# Business Value

Newsentra reduces the time required to:

* Research news
* Compare sources
* Understand events
* Generate reports
* Create executive summaries

The platform transforms large volumes of news content into concise, structured, and actionable insights.

---

# Conclusion

Newsentra is an intelligent news research platform that combines multi-source news aggregation with modern LLM-powered summarization. By integrating trusted news providers, analytics, translation, sentiment analysis, and export capabilities into a single application, Newsentra enables users to consume and analyze news faster, more accurately, and more efficiently.
