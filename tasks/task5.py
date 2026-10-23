
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Take inputs from the user
topic = input("Enter post topic: ")
platform = input("Enter platform (Twitter / LinkedIn / Instagram): ")
tone = input("Enter tone (professional / friendly / funny / inspirational): ")

# Template: topic + platform + tone
prompt_template = """
Create a social media post using these details:

Topic: {topic}
Platform: {platform}
Tone: {tone}

Requirements:
- Match the writing style to the selected platform.
- Include relevant hashtags.
- Keep the post within the platform's usual content length.
- Use the requested tone.
- Make the post engaging and easy to understand.
"""

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.7,
    max_tokens=400,
    messages=[
        {
            "role": "system",
            "content": """
            You are a professional social media content creator.

            Follow these platform-specific examples:

            Example 1 - Twitter:
            Topic: Healthy habits
            Tone: Friendly
            Output:
            Small habits make a big difference! 💚
            Drink water, take a walk, and give yourself time to rest.
            #HealthyHabits #DailyWellness

            Example 2 - LinkedIn:
            Topic: Teamwork
            Tone: Professional
            Output:
            Strong teamwork drives meaningful results.
            When people share ideas and support one another,
            teams can achieve more together.
            #Teamwork #Leadership #ProfessionalGrowth

            Example 3 - Instagram:
            Topic: Travel
            Tone: Inspirational
            Output:
            Collect moments, not things. ✈️🌍
            Every journey brings a new story and a fresh perspective.
            Where will you go next?
            #TravelGoals #ExploreTheWorld #Adventure

            Rules:
            - Twitter: Keep the post short and engaging.
            - LinkedIn: Use a professional style and meaningful insights.
            - Instagram: Make it visually appealing with emojis
              when suitable and relevant hashtags.
            - Follow the user's requested tone.
            - Generate content relevant to the topic.
            - Do not copy the examples directly.
            - Return only the generated post.
            """
        },
        {
            "role": "user",
            "content": prompt_template.format(
                topic=topic,
                platform=platform,
                tone=tone
            )
        },
    ]
)

print("\n--- GENERATED SOCIAL MEDIA POST ---\n")
print(response.choices[0].message.content.strip())
