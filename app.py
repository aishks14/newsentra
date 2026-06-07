import traceback

import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

from datetime import (
    datetime,
    date,
    timedelta
)

from textblob import TextBlob
from news.aggregator import (
    fetch_all_news
)

from llm.summarizer import (
    generate_summary
)

from translation.translator import (
    translate_text
)

from export.pdf_export import (
    create_pdf
)

from export.txt_export import (
    create_txt
)

from config.language_config import (
    LANGUAGES
)

from utils.helpers import (
    filter_articles_by_date,
    filter_relevant_articles
)

from config.categories import (
    CATEGORIES,
    CATEGORY_KEYWORDS
)

DEFAULT_NEWS_IMAGE = (
    "https://images.unsplash.com/photo-1504711434969-e33886168f5c"
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Global News Research Tool",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================

DEFAULT_STATE = {

    "articles": [],
    "summary": "",
    "translated_summary": "",
    "search_query": "",
    "selected_language": "English",
    "show_articles": True,
    "theme_mode": "Light",
    "model_used":
        "llama-3.3-70b-versatile",
    "last_search_time": 0,
    "search_completed": False,
    "pending_query": "",
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value

dark_mode = st.session_state.get(
    "theme_mode",
    "Light"
) == "Dark"

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
<style>

.block-container{
    padding-top:2rem;
    max-width:980px;
    margin:auto;
}

/* ------------------------------------------------ */
/* Header */
/* ------------------------------------------------ */

.app-header{
    text-align:center;
    margin-bottom:30px;
}

.app-title{
    font-size:48px;
    font-weight:700;
}

.app-subtitle{
    color:#6b7280;
    font-size:18px;
}

.hero-section{
    text-align:center;
    margin-bottom:40px;
}

.hero-title{
    font-size:36px;
    font-weight:600;
    text-align:center;
    margin-bottom:30px;
}

.chat-box{
    border:1px solid #d1d5db;
    border-radius:28px;
    padding:25px;
    background:white;
    margin-bottom:30px;
    box-shadow:
    0 4px 12px rgba(
        0,
        0,
        0,
        0.05
    );
}

/* ------------------------------------------------ */
/* Search Input */
/* ------------------------------------------------ */

.stChatInput {
    width: 100% !important;
}

/* ChatGPT Style Search Box */

div[data-testid="stChatInput"] {
    background: white !important;
    border: 1px solid #d1d5db !important;
    border-radius: 32px !important;
    box-shadow:
        0 2px 8px rgba(
            0,
            0,
            0,
            0.05
        ) !important;

    padding: 6px 12px !important;
}

div[data-testid="stChatInput"]:focus-within {
    border: 1px solid #2563eb !important;
    box-shadow:
        0 0 0 2px rgba(
            37,
            99,
            235,
            0.15
        ) !important;
}

div[data-testid="stChatInput"] textarea {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    font-size: 18px !important;
}

/* ------------------------------------------------ */
/* Analytics Cards */
/* ------------------------------------------------ */

.source-pill {
    display:inline-block;
    padding:4px 10px;
    margin-right:6px;
    border-radius:14px;
    background:#eef2ff;
    border:1px solid #c7d2fe;
    color:#4b5563;
    font-size:12px;
    font-weight:500;
}

.metric-card {
    background: linear-gradient(
        135deg,
        #1f2937,
        #374151
    );

    color: white;
    border-radius: 0px;
    padding: 20px;
    text-align: center;
    margin-bottom: 15px;
    box-shadow:
        10px 5px 15px gray;
}

.metric-title {
    font-size: 14px;
    color: #d1d5db;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
}

/* ------------------------------------------------ */
/* Summary */
/* ------------------------------------------------ */

.summary-box{
    padding:25px;
    border-radius: 0px;
    background:#f8fafc;
    border:1px solid #e5e7eb;
    box-shadow: 0 4px 12px rgba(
        0,
        0,
        0,
        0.05
    );
}

/* ------------------------------------------------ */
/* Articles */
/* ------------------------------------------------ */

.article-meta{
    color:#6b7280;
    font-size:13px;
}

/* ------------------------------------------------ */
/* Expander */
/* ------------------------------------------------ */

.stExpander {
    border-radius: 0px !important;
    box-shadow: 0px 0px 5px 0px #bcb8b8
}

.stExpander details {
    border: 1px solid #e5e7eb !important;
    border-radius: 0px !important;
}

/* ------------------------------------------------ */
/* Footer */
/* ------------------------------------------------ */

.footer{
    text-align:center;
    color:#9ca3af;
    padding-top:20px;
}


/* ===================================== */
/* Sidebar Width */
/* ===================================== */

section[data-testid="stSidebar"] {
    width: 280px !important;
    min-width: 280px !important;
}

section[data-testid="stSidebar"] > div {
    width: 280px !important;
}

/* ===================================== */
/* Main Content Width */
/* ===================================== */

.main-content {
    max-width: 980px;
    margin: auto;
}

</style>
""",
    unsafe_allow_html=True
)

# ==================================
# DARK MODE CSS OVERRIDE
# ==================================

if st.session_state.get(
    "theme_mode",
    "Light"
) == "Dark":

    st.markdown(
        """
        <style>

        .stApp,
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a !important;
            color: white !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #111827 !important;
        }

        h1,h2,h3,h4,h5,h6,
        p,
        span,
        label,
        div {
            color: white !important;
        }

        .metric-card {
            background: #1e293b !important;
            border: 1px solid #334155 !important;
            color: white !important;
            box-shadow: none !important;
        }

        .metric-title {
            color: #e2e8f0 !important;
        }

        .metric-value {
            color: #ffffff !important;
        }

        .summary-box {
            background: #1e293b !important;
            border: 1px solid #334155 !important;
            color: white !important;
        }

        .article-meta {
            color: #cbd5e1 !important;
        }

        .footer {
            color: #cbd5e1 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# HEADER
# =====================================================

# st.markdown(
#     """
# <div class="app-header">

# <div class="app-title">
# 📰 Global News Research Tool
# </div>

# <div class="app-subtitle">
# Search, Analyze and Summarize News Worldwide
# </div>

# </div>
# """,
#     unsafe_allow_html=True
# )

current_hour = pd.Timestamp.now().hour

if current_hour < 12:
    greeting = "Good Morning"
elif current_hour < 17:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def calculate_sentiment(text):
    try:
        score = (
            TextBlob(text)
            .sentiment
            .polarity
        )
        if score > 0.1:
            return "Positive"
        elif score < -0.1:
            return "Negative"
        return "Neutral"
    except Exception:
        return "Unknown"

def extract_sources(articles):
    sources = []
    for article in articles:
        source = article.get(
            "source",
            {}
        )

        if isinstance(source, dict):
            source_name = source.get(
                "name",
                "Unknown"
            )

        elif isinstance(source, str):
            source_name = source

        else:
            source_name = (
                article.get("source_name")
                or article.get("source_id")
                or "Unknown"
            )

        # ADD SOURCE TO LIST
        sources.append(
            source_name
        )

    return list(
        set(sources)
    )

def build_dataframe(articles):
    rows = []
    for article in articles:
        rows.append({
            "title":
                article.get(
                    "title",
                    ""
                ),
            "publishedAt":
                article.get(
                    "publishedAt",
                    article.get(
                        "pubDate",
                        ""
                    )
                ),
            "url":
                article.get(
                    "url",
                    ""
                )
        })

    return pd.DataFrame(rows)

def count_countries(text):
    countries = [

        "India",
        "USA",
        "China",
        "Russia",
        "Germany",
        "France",
        "Japan",
        "Brazil",
        "Canada",
        "UK"
    ]

    count = 0
    for country in countries:
        if country.lower() in text.lower():
            count += 1
    return count


def metric_card(title, value):

    st.markdown(
        f"""
<div class="metric-card">
<div class="metric-title">{title}</div>
<div class="metric-value">{value}</div>
</div>
""",
        unsafe_allow_html=True
    )


# =====================================================
# LANDING PAGE SEARCH
# =====================================================

current_hour = datetime.now().hour

if current_hour < 12:
    greeting = "Good Morning"
elif current_hour < 17:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

search_button = False
selected_language = (
    st.session_state.get(
        "selected_language",
        "English"
    )
)

if not st.session_state.search_completed:

    st.markdown(
        f"""
        <h2 style="
            text-align:center;
            margin-top:180px;
            font-size:36px;
            font-weight:600;
        ">
            {greeting}, Stay informed with Newsentra!
        </h2>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [1, 3, 1]
    )

    with col2:

        query = st.chat_input(
            "Ask anything about world news..."
        )

else:
    query = None
# else:
#     query = st.session_state.get(
#         "search_query",
#         ""
#     )

# =====================================================
# FILTERS ROW
# =====================================================

# categories = [
#     "General",
#     "Politics",
#     "Business",
#     "Technology",
#     "Sports",
#     "Entertainment",
#     "Health",
#     "Science",
#     "Environment",
#     "Weather",
#     "Disasters",
#     "Military",
#     "Finance",
#     "Education"
# ]

# today = date.today()

# if not st.session_state.search_completed:

#     left, center, right = st.columns(
#     [1, 5, 1]
# )

#     with center:
#         control1, control2, control3, control4 = (
#             st.columns(
#                 [2,2,2,1]
#             )
#         )

#         with control1:
#             category = st.selectbox(
#                 "",
#                 categories,
#                 label_visibility="collapsed"
#             )

#         with control2:
#             selected_language = st.selectbox(
#                 "",
#                 list(LANGUAGES.keys()),
#                 label_visibility="collapsed"
#             )
            
#             st.session_state.selected_language = (
#                 selected_language
#             )

#         with control3:
#             date_range = st.date_input(
#                 "",
#                 (
#                     today - timedelta(days=7),
#                     today
#                 ),
#                 label_visibility="collapsed"
#             )

#             if len(date_range) == 2:
#                 from_date = date_range[0]
#                 to_date = date_range[1]

#             else:
#                 from_date = (
#                     today - timedelta(days=7)
#                 )
#                 to_date = today

#         with control4:
#             search_button = st.button(
#                 "Search",
#                 use_container_width=True
#             )

# =====================================================
# SIDEBAR SETTINGS
# =====================================================

with st.sidebar:

    st.header("⚙️ Settings")

    st.subheader(
        "🔍 Search Filters"
    )


    category = st.selectbox(
        "Category",
        list(CATEGORIES.keys())
    )

    selected_language = st.selectbox(
        "Language",
        list(LANGUAGES.keys())
    )

    today = date.today()

    date_range = st.date_input(
        "Date Range",
        (
            today - timedelta(days=7),
            today
        )
    )

    if len(date_range) == 2:

        from_date = date_range[0]
        to_date = date_range[1]

    else:

        from_date = (
            today - timedelta(days=7)
        )

        to_date = today

    st.divider()
    
    dark_mode = st.toggle(
        "Dark Mode",
        value=
        st.session_state.get(
            "theme_mode",
            "Light"
        ) == "Dark"
    )

    st.session_state.theme_mode = (
        "Dark"
        if dark_mode
        else "Light"
    )

    st.divider()

    show_articles = st.toggle(
        "Show Articles",
        value=True
    )

    st.session_state.show_articles = (
        show_articles
    )

    max_articles = st.slider(
        "Maximum Articles",
        5,
        20,
        10
    )

    st.divider()

    st.subheader("LLM")

    selected_model = st.selectbox(
        "Choose Model",
        [
            "llama-3.3-70b-versatile",
            "gemma2-9b-it",
            "llama-3.1-8b-instant",
            "deepseek-r1-distill-llama-70b",
            "deepseek-r1-distill-llama-13b"   
        ]
    )

    st.session_state.model_used = (
        selected_model
    )

    st.divider()

    st.subheader("Session")

    st.write(
        f"Theme: {st.session_state.theme_mode}"
    )

    st.write(
        f"Language: {st.session_state.get('selected_language', 'English')}"
    )

    st.write(
        f"Model: {st.session_state.get('model_used', 'llama-3.3-70b-versatile')}"
    )
# =====================================================
# SEARCH EXECUTION
# =====================================================
if "query" not in locals():
    query = ""

search_button = locals().get(
    "search_button",
    False
)

if (
    query
    or
    st.session_state.pending_query
):
    if not query:
        query = (
            st.session_state.pending_query
        )

    st.session_state.pending_query = ""
    if not query.strip():
        st.warning(
            "Please enter a search query."
        )

    else:
        with st.spinner(
            "Collecting news articles..."
        ):
            start_time = time.time()

            try:
                # ----------------------------------
                # Search Query
                # ----------------------------------

                category_keywords = (
                    CATEGORY_KEYWORDS.get(
                        category,
                        ""
                    )
                )

                if category_keywords:
                    search_query = (
                        f"{query} {category_keywords}"
                    )

                else:
                    search_query = query

                st.session_state.search_query = (
                    search_query
                )

                lang_config = (
                    LANGUAGES[
                        selected_language
                    ]
                )

                # ----------------------------------
                # Fetch News
                # ----------------------------------

                print(
                    "SELECTED LANGUAGE:",
                    selected_language
                )

                print(
                    "LANGUAGE CODE:",
                    lang_config["newsapi"]
                )

                print(
                    "LANGUAGE TYPE:",
                    type(lang_config["newsapi"])
                )
                
                articles, source_counts = (
                    fetch_all_news(
                        query=search_query,
                        lang_label=selected_language,
                        lang_code=lang_config[
                            "newsapi"
                        ],
                        gnews_lang=lang_config[
                            "gnews"
                        ],

                        nd_lang=lang_config[
                            "nd"
                        ],
                        category_label=category,
                        from_date=from_date,
                        to_date=to_date,
                        max_articles=max_articles,
                        sort_by="relevancy"
                    )
                )
                
                st.session_state.source_counts = (
                    source_counts
                )
                                                
                if not articles:
                    st.warning(
                        "No relevant articles found."
                    )
                    st.stop()
                
                # articles = filter_relevant_articles(
                #     articles,
                #     query
                # )

                # ----------------------------------
                # Date Filtering
                # ----------------------------------

                # articles = filter_articles_by_date(
                #     articles,
                #     from_date,
                #     to_date
                # )
                
                # st.write(
                #     "Articles after date filter:",
                #     len(articles)
                # )

                # ----------------------------------
                # Sort Latest First
                # ----------------------------------

                articles.sort(
                    key=lambda x:
                    x.get(
                        "publishedAt"
                    )
                    or
                    x.get(
                        "pubDate",
                        ""
                    ),

                    reverse=True
                )

                # ----------------------------------
                # Remove Duplicates
                # ----------------------------------

                unique_articles = []
                seen_urls = set()
                for article in articles:
                    url = article.get(
                        "url",
                        ""
                    )

                    if (
                        url
                        and url
                        not in seen_urls
                    ):

                        unique_articles.append(
                            article
                        )

                        seen_urls.add(
                            url
                        )

                st.session_state.articles = (
                    unique_articles[
                        :max_articles
                    ]
                )

                # ----------------------------------
                # Summary Generation
                # ----------------------------------

                recent_articles = (
                    st.session_state.articles[:40]
                )

                summary = generate_summary(
                    search_query,
                    recent_articles,
                    st.session_state.model_used
                )

                st.session_state.summary = (
                    summary
                )

                # ----------------------------------
                # Translation
                # ----------------------------------

                translated_summary = (
                    translate_text(
                        summary,
                        lang_config["tr"]
                    )
                )

                st.session_state.translated_summary = (
                    translated_summary
                )

                # ----------------------------------
                # Timing
                # ----------------------------------

                end_time = time.time()

                st.session_state.last_search_time = (
                    round(
                        end_time
                        - start_time,
                        2
                    )
                )

                st.session_state.search_completed = (
                    True
                )

                st.toast(
                    f"Found {len(st.session_state.articles)} articles"
                )

            except Exception as e:
                st.error(
                    f"""
            Type: {type(e).__name__}

            Message: {str(e)}
            """
                )

                st.code(
                    traceback.format_exc()
                )

# =====================================================
# TRANSLATION REFRESH
# =====================================================

if (
    st.session_state.summary
    and selected_language
):

    try:

        target_lang = (
            LANGUAGES[
                selected_language
            ]["tr"]
        )

        st.session_state.translated_summary = (
            translate_text(
                st.session_state.summary,
                target_lang
            )
        )

    except Exception:

        st.session_state.translated_summary = (
            st.session_state.summary
        )

# =====================================================
# ANALYTICS CALCULATIONS
# =====================================================

articles = st.session_state.articles

summary = (
    st.session_state.translated_summary
)

total_articles = len(
    articles
)

source_list = extract_sources(
    articles
)

source_count = len(
    source_list
)

country_count = count_countries(
    summary
)

sentiment = calculate_sentiment(
    summary
)

word_count = (
    len(summary.split())
    if summary
    else 0
)

reading_time = round(
    word_count / 200,
    1
)

estimated_tokens = round(
    word_count * 1.3
)

response_time = (
    st.session_state.last_search_time
)

model_used = (
    st.session_state.model_used
)

# =====================================================
# ANALYTICS CARDS
# =====================================================

if summary:

    st.markdown(
        '<div class="main-content">',
        unsafe_allow_html=True
    )
    st.divider()
    st.subheader(
        "📊 News Analytics"
    )

    row1 = st.columns(4)

    with row1[0]:
        metric_card(
            "Articles",
            total_articles
        )

    with row1[1]:
        metric_card(
            "News Sources",
            source_count
        )

    with row1[2]:
        metric_card(
            "Countries",
            country_count
        )

    with row1[3]:
        metric_card(
            "Sentiment",
            sentiment
        )

    row2 = st.columns(4)

    with row2[0]:
        metric_card(
            "Summary Words",
            word_count
        )

    with row2[1]:
        metric_card(
            "Reading Time",
            f"{reading_time} min"
        )

    with row2[2]:
        metric_card(
            "Tokens",
            estimated_tokens
        )

    with row2[3]:
        metric_card(
            "Response Time",
            f"{response_time}s"
        ) 
        
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =====================================================
# MODEL & SOURCE INFO PILLS
# =====================================================

if (
    "source_counts"
    in st.session_state
):

    pills = ""

    provider_html = ""

    for source, count in (
        st.session_state.source_counts.items()
    ):

        provider_html += f"""
        <span class='source-pill'>
            {source}: {count}
        </span>
        """

    st.markdown(
        f"""
        <div style="
            margin-top:10px;
            margin-bottom:10px;
        ">
            <span style="
                font-size:14px;
                font-weight:600;
                margin-right:10px;
            ">
                API Source Distribution:
            </span>

            {provider_html}
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# DATAFRAME
# =====================================================

try:

    article_df = (
        build_dataframe(
            articles
        )
    )

except Exception:

    article_df = pd.DataFrame()

# =====================================================
# SOURCE ANALYTICS
# =====================================================

source_frequency = {}

for article in articles:

    source = article.get(
            "source",
            {}
        )

    if isinstance(source, dict):
        source_name = source.get(
            "name",
            "Unknown"
        )
    
    elif isinstance(source, str):
        source_name = source

    else:
        source_name = (
            article.get(
                "source_name"
            )
            or
            article.get(
                "source_id"
            )
            or
            "Unknown"
        )

    source_frequency[
        source_name
    ] = (
        source_frequency.get(
            source_name,
            0
        )
        + 1
    )

source_df = pd.DataFrame(
    {

        "Source":
            list(
                source_frequency.keys()
            ),

        "Articles":
            list(
                source_frequency.values()
            )
    }
)

if not source_df.empty:

    source_df = (
        source_df.sort_values(
            by="Articles",
            ascending=False
        )
    )

# =====================================================
# TIMELINE ANALYTICS
# =====================================================

timeline_data = []

for article in articles:

    article_date = (

        article.get(
            "publishedAt",
            ""
        )

        or

        article.get(
            "pubDate",
            ""
        )
    )

    if article_date:

        timeline_data.append(
            {
                "date":
                    article_date[:10]
            }
        )

timeline_df = pd.DataFrame(
    timeline_data
)

if not timeline_df.empty:

    timeline_df = (
        timeline_df.groupby(
            "date"
        )
        .size()
        .reset_index(
            name="articles"
        )
    )

# =====================================================
# DOWNLOAD FILES
# =====================================================

pdf_file = None

txt_file = None

if summary:

    try:

        pdf_file = (
            create_pdf(
                summary
            )
        )

    except Exception as e:
        st.error(
            f"PDF Error: {e}"
        )

        print(
            "PDF ERROR:",
            e
        )

    try:

        txt_file = (
            create_txt(
                summary
            )
        )

    except Exception:
        pass

# =====================================================
# CHAT CONVERSATION
# =====================================================

st.markdown(
    """
    <style>
    .main-content {
        max-width: 1000px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-content">',
    unsafe_allow_html=True
)

if summary:

    st.divider()
    # User Message
    with st.chat_message("user"):

        st.write(
            st.session_state.search_query
        )

    # Assistant Message
    with st.chat_message("assistant"):
        st.markdown(
            f"""
            <div class="summary-box">
            {summary}
            </div>
            """,
            unsafe_allow_html=True
        )
        
# =====================================================
# EXPORT SECTION
# =====================================================

if summary:

    st.divider()

    st.subheader(
        "⬇️ Export Summary"
    )

    export_col1, export_col2 = (
        st.columns(2)
    )

    with export_col1:

        if (
            txt_file
            and
            os.path.exists(
                txt_file
            )
        ):

            with open(
                txt_file,
                "rb"
            ) as file:

                st.download_button(
                    "Download TXT",
                    file,
                    "news_summary.txt",
                    "text/plain",
                    use_container_width=True
                )

    with export_col2:
        if (
            pdf_file
            and
            os.path.exists(
                pdf_file
            )
        ):

            with open(
                pdf_file,
                "rb"
            ) as file:

                st.download_button(
                    "Download PDF",
                    file,
                    "news_summary.pdf",
                    "application/pdf",
                    use_container_width=True
                )  


# =====================================================
# CHARTS
# =====================================================

if summary:

    st.divider()

    st.subheader(
        "📈 Analytics Dashboard"
    )

    chart_col1, chart_col2 = (
        st.columns(2)
    )

    with chart_col1:

        if not source_df.empty:

            fig_sources = px.bar(
                source_df.head(
                    10
                ),
                x="Source",
                y="Articles",
                title="Top Sources"
            )

            st.plotly_chart(
                fig_sources,
                use_container_width=True
            )

    with chart_col2:

        if not timeline_df.empty:

            fig_timeline = px.line(
                timeline_df,
                x="date",
                y="articles",
                markers=True,
                title="News Timeline"
            )

            st.plotly_chart(
                fig_timeline,
                use_container_width=True
            )

# =====================================================
# SOURCE TABLE
# =====================================================

if not source_df.empty:
    st.divider()
    st.subheader(
        "🏢 Source Breakdown"
    )

    st.dataframe(
        source_df,
        use_container_width=True
    )

# =====================================================
# ARTICLE DISPLAY
# =====================================================

if (

    st.session_state.show_articles

    and

    articles

):

    st.divider()

    st.subheader(
        f"📰 Articles ({len(articles)})"
    )

    for idx, article in enumerate(
        articles,
        start=1
    ):

        title = article.get(
            "title",
            "No Title"
        )

        source = article.get(
            "source",
            {}
        )

        if isinstance(source, dict):
            source_name = source.get(
                "name",
                "Unknown"
            )
        
        elif isinstance(source, str):
            source_name = source

        else:
            source_name = (
                article.get(
                    "source_name"
                )
                or
                article.get(
                    "source_id"
                )
                or
                "Unknown"
            )

        published = (

            article.get(
                "publishedAt",
                ""
            )

            or

            article.get(
                "pubDate",
                ""
            )
        )

        description = (

            article.get(
                "description",
                ""
            )

            or

            article.get(
                "content",
                ""
            )

            or

            "No Description Available"
        )

        article_url = (
            article.get("url")
            or article.get("link")
            or article.get("article_url")
            or ""
        )

        sentiment_value = (
            calculate_sentiment(
                description
            )
        )

        with st.expander(
            f"{idx}. {title}"
        ):

            left, right = st.columns(
                [3, 2]
            )

            with left:
                st.markdown(
                    f"**{source_name}** | 📅 {published[:10]}"
                )

                st.markdown(
                    f"**Sentiment:** {sentiment_value}"
                )

                short_description = description[:220]
                if len(description) > 220:
                    short_description += "..."

                st.write(short_description)
                
                if article_url:

                    st.link_button(
                        "📰 Read Full Article",
                        article_url,
                        use_container_width=False
                    )

            with right:

                image_url = (
                    article.get("image")
                    or DEFAULT_NEWS_IMAGE
                )

                st.image(
                    image_url,
                    use_container_width=True
                )

# =====================================================
# FOLLOW UP SEARCH
# =====================================================
st.markdown(
    """
    <style>

    div[data-testid="stChatInput"] {
        position: fixed !important;
        left: 60% !important;
        transform: translateX(-50%);
        width: 60% !important;
        z-index: 9999 !important;
        background: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

if st.session_state.search_completed:

    st.markdown(
        """
        <style>

        div[data-testid="stChatInput"] {
            position: fixed;
            bottom: 20px;
            left: 340px;
            right: 40px;
            z-index: 999;
            background: white;
            padding-top: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    prompt = st.chat_input(
        "Ask a follow-up question...",
        key="bottom_search"
    )

    if prompt:

        st.session_state.pending_query = (
            prompt
        )

        st.session_state.search_completed = (
            False
        )

        st.rerun()