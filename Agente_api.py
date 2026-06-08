import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
openai = OpenAI()

system_prompt = """You are a financial analyst specializing in capital markets.

Your role is to analyze data, indicators, news, and corporate announcements extracted from financial sources and transform them into clear, 
objective, and useful insights. Don't just repeat information; interpret the data, identify causes and possible consequences, explain the 
factors that influenced price movements, highlight risks, opportunities, and trends, and connect market events to their potential impacts in the
short, medium, and long term. Always present a brief summary of the scenario, the main factors influencing it, relevant insights, and points 
of attention. Adapt the depth of the analysis to the available context, considering financial indicators when applicable. Maintain professional
and accessible language, avoiding direct buy or sell recommendations, focusing on well-founded analysis and informed decision-making. 
Finally, provide a concise executive conclusion and a sentiment rating of the news or event on a scale of -10 (very negative) to +10 
(very positive), briefly justifying the assessment.
"""

def messages_for(website_content):
    user_prompt = f"""Here are the contents of a website. Provide a short summary of this website. 
                    If it includes news or announcements, then summarize these too. {website_content}"""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def summarize(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages_for(website)
    )
    return response.choices[0].message.content

def display_summary(url):
    summary = summarize(url)
    print(summary)

display_summary("https://www.infomoney.com.br/")
