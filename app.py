from preswald import text, plotly, connect, get_df, table, query
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

# Title and Description
text("# 📊 Laptop Reviews Analysis Dashboard")
text("### Comprehensive analysis of 24,000 Laptop reviews")
text("This dashboard explores ratings, popular products, and review content patterns. The data is obtained from Kaggle.")

# Load the data
connect()
df = get_df('reviews_csv')

# Display a sample of the data
sql_sample = "SELECT * FROM reviews_csv ORDER BY RANDOM() LIMIT 10"
sample_df = query(sql_sample, "reviews_csv")
table(sample_df, title="📋 Sample Review Data")

from preswald import slider
threshold = slider("Ratings Threshold", min_val=0, max_val=5, default=0)
table(df[df["rating"] > threshold], title="Dynamic Data View")

# Color palette for consistent design
colors = ['#4361ee', '#3a0ca3', '#7209b7', '#f72585', '#4cc9f0', '#560bad', '#f77f00']

# ------- SECTION 1: BASIC RATING ANALYSIS -------

text("## 📈 Rating Distribution and Trends")

# Chart 1: Rating Distribution
fig_rating = px.histogram(
    df, 
    x="rating",
    nbins=5,
    color_discrete_sequence=[colors[0]],
    title="Rating Distribution",
    labels={"rating": "Rating Value", "count": "Number of Reviews"},
    opacity=0.8
)

# Add average line
avg_rating = df['rating'].mean()
fig_rating.add_vline(
    x=avg_rating, 
    line_dash="dash", 
    line_color=colors[3], 
    annotation_text=f"Avg: {avg_rating:.2f}", 
    annotation_position="top right"
)

fig_rating.update_layout(
    xaxis=dict(tickvals=[1, 2, 3, 4, 5]),
    bargap=0.1,
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)'
)
plotly(fig_rating)

# ------- SECTION 2: PRODUCT ANALYSIS -------

text("## 🔍 Product Analysis")

# Chart 2: Most Reviewed Products
top_products = df.groupby("product_name").size().reset_index(name="review_count")
top_products = top_products.sort_values("review_count", ascending=False).head(10)

fig_top = px.bar(
    top_products, 
    x="review_count", 
    y="product_name", 
    color="review_count",
    color_continuous_scale=[colors[1], colors[2]],
    title="Top 10 Most Reviewed Laptops",
    labels={"product_name": "Product", "review_count": "Number of Reviews"},
    orientation='h'
)

fig_top.update_layout(
    yaxis={'categoryorder':'total ascending'},
    coloraxis_showscale=False,
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_top.update_traces(texttemplate='%{x}', textposition='outside')
plotly(fig_top)

# Chart 3: Top-Rated Products (with minimum 20 reviews)
avg_rating_df = df.groupby("product_name").agg(
    avg_rating=("rating", "mean"), 
    count=("rating", "size")
).reset_index()
avg_rating_df = avg_rating_df[avg_rating_df["count"] >= 20]
avg_rating_df = avg_rating_df.sort_values("avg_rating", ascending=False).head(10)

fig_avg = make_subplots(specs=[[{"secondary_y": True}]])

# Add bars for average rating
fig_avg.add_trace(
    go.Bar(
        x=avg_rating_df["product_name"],
        y=avg_rating_df["avg_rating"],
        name="Avg Rating",
        marker_color=colors[2],
        text=avg_rating_df["avg_rating"].round(2),
        textposition="inside",
    ),
    secondary_y=False,
)

# Add scatter points for review count
fig_avg.add_trace(
    go.Scatter(
        x=avg_rating_df["product_name"],
        y=avg_rating_df["count"],
        name="Review Count",
        mode="markers",
        marker=dict(
            color=colors[4],
            size=avg_rating_df["count"]/10 + 10,
            opacity=0.7,
        ),
    ),
    secondary_y=True,
)

fig_avg.update_layout(
    title="Top 10 Highest Rated Laptops (min 20 reviews)",
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(tickangle=45),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# fig_avg.update_yaxes(title_text="Average Rating", secondary_y=False, range=[min(avg_rating_df["avg_rating"])-0.5, 5])
# Update the y-axis range to start closer to your minimum value
fig_avg.update_yaxes(title_text="Average Rating", secondary_y=False, range=[4.6, 5.5])
fig_avg.update_yaxes(title_text="Number of Reviews", secondary_y=True)
plotly(fig_avg)

text("The visualization reveals several key insights about top-rated laptops:\n\n" +
     "1. The Primebook 4G Android-based MediaTek MT8788 leads with the highest rating of 4.95, significantly above competitors, suggesting exceptional customer satisfaction.\n\n" +
     "2. Apple dominates the top spots with two MacBook Air models (4.84 and 4.82 ratings), indicating strong brand performance in the premium laptop segment.\n\n" +
     "3. An interesting correlation appears between review count and ratings - some highly-rated models have relatively few reviews (like the Primebook and Apple models with ~100 reviews), while others like Samsung Galaxy Book4 and ASUS Vivobook have 250-300 reviews but slightly lower ratings.\n\n" +
     "4. The ratings are tightly clustered between 4.73-4.95, showing fierce competition in the high-end laptop market with minimal differences separating the top contenders.\n\n" +
     "5. Intel and AMD processors appear equally represented in the top-rated laptops, suggesting both manufacturers are producing competitive chips that satisfy users.")


# Chart 4: Rating Distribution by Top 5 Products
top5_products = df.groupby("product_name").size().reset_index(name="count")
top5_products = top5_products.sort_values("count", ascending=False).head(5)
top5_df = df[df["product_name"].isin(top5_products["product_name"])]

fig_dist = px.histogram(
    top5_df,
    x="rating",
    color="product_name",
    barmode="group",
    title="Rating Distribution for Top 5 Most Popular Laptops",
    labels={"rating": "Rating", "count": "Number of Reviews", "product_name": "Product"},
    color_discrete_sequence=colors,
    nbins=5
)

fig_dist.update_layout(
    xaxis=dict(tickvals=[1, 2, 3, 4, 5]),
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)',
    bargap=0.2
)
plotly(fig_dist)



# ------- SECTION 3: REVIEW TEXT ANALYSIS -------

text("## 📝 Review Content Analysis")

# Function to extract review length
def get_review_length(text):
    if isinstance(text, str):
        return len(text.split())
    return 0

# Add review length to dataframe
df['review_length'] = df['review'].apply(get_review_length)

# Chart 5: Review Length Distribution
fig_length = px.histogram(
    df, 
    x="review_length",
    nbins=30,
    color_discrete_sequence=[colors[5]],
    title="Distribution of Review Lengths",
    labels={"review_length": "Number of Words", "count": "Number of Reviews"}
)

# Add median line
median_length = df['review_length'].median()
fig_length.add_vline(
    x=median_length, 
    line_dash="dash", 
    line_color=colors[3], 
    annotation_text=f"Median: {median_length:.0f} words", 
    annotation_position="top right"
)

fig_length.update_layout(
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)'
)
plotly(fig_length)

# Chart 6: Review Length vs. Rating
fig_length_rating = px.box(
    df,
    x="rating",
    y="review_length",
    color="rating",
    title="Review Length by Rating",
    labels={"rating": "Rating", "review_length": "Review Length (words)"},
    color_discrete_sequence=colors
)

fig_length_rating.update_layout(
    xaxis=dict(tickvals=[1, 2, 3, 4, 5]),
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False
)
plotly(fig_length_rating)



# Chart 7: Simple word frequency analysis (without NLTK)
# Function to extract simple word frequency without NLTK
def count_word_frequency(text_series, max_words=1000):
    # Convert series to list of strings
    text_list = text_series.dropna().astype(str).tolist()
    
    # Sample to avoid processing all 24,000 reviews
    import random
    if len(text_list) > max_words:
        text_list = random.sample(text_list, max_words)
    
    # Split into words and convert to lowercase
    words = []
    for text in text_list:
        words.extend([word.lower() for word in re.findall(r'\b[a-zA-Z]{3,}\b', text)])
    
    # Count word frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Return top 20 words
    return sorted_words[:20]

# Get word frequency
common_words = count_word_frequency(df['review'], max_words=1000)
common_words_df = pd.DataFrame(common_words, columns=['word', 'count'])

# Filter out common stopwords manually
stopwords = ['the', 'and', 'for', 'this', 'that', 'with', 'you', 'not', 'have', 'are', 'was', 
             'very', 'its', 'has', 'from', 'but', 'all', 'can', 'will', 'when', 'than', 'just']
common_words_df = common_words_df[~common_words_df['word'].isin(stopwords)]
common_words_df = common_words_df.head(20)

fig_words = px.bar(
    common_words_df,
    x="count",
    y="word",
    orientation='h',
    title="Top 20 Most Common Words in Reviews",
    labels={"word": "Word", "count": "Frequency"},
    color="count",
    color_continuous_scale=[colors[0], colors[6]]
)

fig_words.update_layout(
    yaxis={'categoryorder':'total ascending'},
    coloraxis_showscale=False,
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)'
)
plotly(fig_words)

text("The visualizations reveals several key insights about laptop reviews:\n\n" +
     "1. Most laptop reviews are extremely brief, with the typical review being just 8 words long, suggesting consumers provide quick reactions rather than detailed assessments.\n\n" +
     "2. Review length doesn't vary significantly based on rating—people write similarly brief reviews whether they loved or hated the product, with all rating categories showing similar median lengths.\n\n" +
     "3. The vocabulary is predominantly positive, with 'good' being overwhelmingly the most common word, followed by 'laptop' and 'product', indicating overall satisfaction with the products being reviewed.\n\n" +
     "4. Key product attributes that matter to reviewers include battery, performance, display, price, and value, highlighting the features consumers focus on when evaluating laptops.\n\n" +
     "5. The distribution of review lengths has a long right tail, meaning while most reviews are short, there are some outliers with significantly more content—some reaching 80-100 words across all rating categories.")

# ------- SECTION 4: CORRELATION AND RELATIONSHIPS -------

text("## 🔗 Relationship Analysis")

# Chart 8: Correlation between reviews count and average rating
correlation_df = df.groupby("product_name").agg(
    avg_rating=("rating", "mean"),
    review_count=("rating", "size")
).reset_index()
# Filter for products with at least 20 reviews
correlation_df = correlation_df[correlation_df["review_count"] >= 20]

fig_corr = px.scatter(
    correlation_df,
    x="review_count",
    y="avg_rating",
    size="review_count",
    color="avg_rating",
    color_continuous_scale=colors,
    hover_name="product_name",
    title="Relationship between Number of Reviews and Average Rating",
    labels={"avg_rating": "Average Rating", "review_count": "Number of Reviews"},
    size_max=30,
)

fig_corr.update_layout(
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)'
)
plotly(fig_corr)

# Chart 9: Rating trends over time (if we can extract date from titles or make assumption)
# For demonstration purposes, let's assume reviews are in chronological order and create a time index
df['review_index'] = range(len(df))
df['time_bucket'] = pd.qcut(df['review_index'], 10, labels=False)  # Create 10 time buckets

time_trend = df.groupby('time_bucket').agg(
    avg_rating=('rating', 'mean'),
    count=('rating', 'size')
).reset_index()

fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

fig_trend.add_trace(
    go.Scatter(
        x=time_trend['time_bucket'],
        y=time_trend['avg_rating'],
        mode='lines+markers',
        name='Avg Rating',
        line=dict(color=colors[2], width=3),
        marker=dict(size=8)
    ),
    secondary_y=False
)

fig_trend.add_trace(
    go.Bar(
        x=time_trend['time_bucket'],
        y=time_trend['count'],
        name='Review Count',
        marker_color=colors[0],
        opacity=0.7
    ),
    secondary_y=True
)

fig_trend.update_layout(
    title="Rating Trends Over the Dataset",
    xaxis_title="Time Period (earliest to latest)",
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig_trend.update_yaxes(title_text="Average Rating", secondary_y=False)
fig_trend.update_yaxes(title_text="Number of Reviews", secondary_y=True)
plotly(fig_trend)

# ------- SECTION 5: TITLE ANALYSIS -------

text("## 📊 Title Analysis")

# Chart 10: Average title length by rating
df['title_length'] = df['title'].apply(lambda x: len(str(x).split()) if isinstance(x, str) else 0)

fig_title = px.bar(
    df.groupby('rating').agg(
        avg_title_length=('title_length', 'mean'),
        count=('title_length', 'size')
    ).reset_index(),
    x='rating',
    y='avg_title_length',
    title="Average Title Length by Rating",
    labels={"rating": "Rating", "avg_title_length": "Average Title Length (words)"},
    color='rating',
    color_discrete_sequence=colors,
    text='avg_title_length'
)

fig_title.update_layout(
    xaxis=dict(tickvals=[1, 2, 3, 4, 5]),
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False
)

fig_title.update_traces(texttemplate='%{y:.1f}', textposition='outside')
plotly(fig_title)

# Chart 11: Simple sentiment measure - categorize ratings
df['sentiment'] = pd.cut(
    df['rating'], 
    bins=[0, 2, 3.5, 5], 
    labels=['Negative', 'Neutral', 'Positive']
)

fig_sentiment = px.pie(
    df, 
    names='sentiment', 
    title="Overall Sentiment Distribution",
    color='sentiment',
    color_discrete_map={'Positive': colors[0], 'Neutral': colors[1], 'Negative': colors[3]},
    hole=0.4
)

fig_sentiment.update_layout(
    title_font_size=18,
    plot_bgcolor='rgba(0,0,0,0)'
)
plotly(fig_sentiment)

# Add summary insights
total_products = df['product_name'].nunique()
total_reviews = len(df)
avg_overall = df['rating'].mean()
avg_words = df['review_length'].mean()
max_rated_product = avg_rating_df.iloc[0]['product_name'] if not avg_rating_df.empty else "N/A"
max_rating = avg_rating_df.iloc[0]['avg_rating'] if not avg_rating_df.empty else 0

text(f"""
### 📊 Dashboard Insights Summary

- **Products Analyzed**: {total_products}
- **Total Reviews**: {total_reviews:,}
- **Overall Average Rating**: {avg_overall:.2f}/5.0
- **Average Review Length**: {avg_words:.1f} words
- **Highest Rated Popular Product**: {max_rated_product} ({max_rating:.2f}/5.0)
- **Most Common Rating**: {df['rating'].mode().iloc[0]}
- **Reviews with 5-star Rating**: {(df['rating'] == 5).sum()} ({(df['rating'] == 5).sum()/len(df)*100:.1f}%)
""")