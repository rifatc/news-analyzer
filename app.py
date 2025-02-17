from flask import Flask, request, render_template
import asyncio
from news_analyzer.scrapper import scrape
from news_analyzer.gemini_integration import send_prompt_to_gemini

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # Render the input form from template.
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.form.get("url")
    business_name = request.form.get("business_name")
    if not url or not business_name:
        return "URL and Business Name are required", 400

    # Run the scrape function and get content asynchronously.
    content = asyncio.run(scrape(url))
    
    system_prompt = f"""You are a financial analyst. You are tasked with analyzing news from the internet.
        You'll be given a news article of the company named "{business_name}" in markdown format. The content will contain other irrelevant information.
        Identify the relevant information and analyze the news article.
        Your job is to determine if the news has a negative, positive, neutral, or irrelevant impact on the value of the company.

        The article can have multiple sections with positive and negative news. Analyze the overall impact of the news on the company's value.

        Any adverse news will have a negative impact on the company's value. Favorable news will have a positive impact. News with no discernible effect should be considered neutral. If the news is irrelevant to the company, categorize it as irrelevant.

        Respond in JSON format with the following attributes:
        - "url": The link to the news article.
        - "headline": The headline of the news article.
        - "key_points": An array of key points extracted from the news article.
        - "analysis": Based on the key points, a paragraph summarizing your analysis of the news article.
        - "impact_type": The impact type, which MUST be one of the following values: "positive", "negative", "neutral", or "irrelevant"."""
    
    user_prompt = f"""
        **News Link:**
        [link to the news article]({url})
        **News Article:**

        [Markdown content of a news article here]
        {content}
        """
    
    # Generate the analysis via Gemini.
    result = send_prompt_to_gemini(system_prompt, user_prompt)
    return render_template("analysis.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask webserver on localhost.
