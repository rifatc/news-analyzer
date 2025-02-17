import asyncio

from news_analyzer.gemini_integration import send_prompt_to_gemini
from news_analyzer.scrapper import scrape

async def main():
    url = "https://www.fintechfutures.com/2024/07/bux-sells-uk-subsidiary-bux-financial-services-limited-to-uaes-asseta-holding/"
    business_name = "BUX"

    content = await scrape(url=url)

    system_prompt = f"""You are a financial analyst. You are tasked with analyzing news from the internet.
        You'll be given a news article of the company named "{business_name}" in markdown format. The content will contain other irrelevant information.
        Identify the relevant information and analyze the news article.
        Your job is to determine if the news has a negative, positive, neutral, or irrelevant impact on the value of the company.

        The article can have multiple section with positive and negative news. Analyze the overall impact of the news on the company's value.

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

    gemini_response = send_prompt_to_gemini(system_prompt, user_prompt)
    print("Gemini response: ", gemini_response)

if __name__ == "__main__":
    asyncio.run(main())
