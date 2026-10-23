
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Input multiple customer reviews
reviews = []

num_reviews = int(input("How many reviews do you want to analyze? "))

for i in range(num_reviews):
    review = input(f"Enter review {i + 1}: ")
    reviews.append(review)

# Few-shot classification examples
classification_examples = """
Classify each review as Positive, Negative, or Neutral.

Example 1:
Review: "The product quality is excellent. I love it!"
Classification: Positive

Example 2:
Review: "The delivery was late and the product was damaged."
Classification: Negative

Example 3:
Review: "The product arrived yesterday."
Classification: Neutral

Example 4:
Review: "Good quality, but the price is too high."
Classification: Negative

Example 5:
Review: "It works as expected."
Classification: Neutral

Use the overall sentiment expressed in each review.
Choose exactly one classification per review.
"""

# Classify each review using a loop
classified_reviews = []

for i, review in enumerate(reviews, start=1):
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.1,
        max_tokens=100,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a customer sentiment classification assistant.

                {classification_examples}

                Return only one label:
                Positive, Negative, or Neutral.
                """
            },
            {
                "role": "user",
                "content": f"Classify this customer review:\n{review}"
            }
        ]
    )

    sentiment = response.choices[0].message.content.strip()

    # Validate the returned classification
    if sentiment not in ["Positive", "Negative", "Neutral"]:
        sentiment = "Needs Review"

    classified_reviews.append({
        "review": review,
        "sentiment": sentiment
    })

# Display individual review classifications
print("\n========== REVIEW CLASSIFICATIONS ==========\n")

for i, item in enumerate(classified_reviews, start=1):
    print(f"Review {i}: {item['review']}")
    print(f"Sentiment: {item['sentiment']}\n")

# Prepare review data for the overall summary
summary_input = "\n".join(
    [
        f"Review {i}: {item['review']} "
        f"(Sentiment: {item['sentiment']})"
        for i, item in enumerate(classified_reviews, start=1)
    ]
)

# Zero-shot summary: summarize without summary examples
summary_response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.1,
    max_tokens=500,
    messages=[
        {
            "role": "system",
            "content": """
            You are a business analyst specializing in customer feedback.

            Analyze the supplied customer reviews and classifications.
            Provide an evidence-based overall summary.

            Include:
            1. Overall customer sentiment.
            2. What customers like.
            3. What customers dislike.
            4. Common complaints or recurring themes.
            5. Suggested business improvements.

            Do not invent feedback that is not present in the reviews.
            If a theme is not mentioned, say so.
            Use clear, concise bullet points.
            """
        },
        {
            "role": "user",
            "content": f"""
            Analyze these customer reviews and provide an overall summary:

            {summary_input}
            """
        }
    ]
)

print("========== OVERALL CUSTOMER SUMMARY ==========\n")
print(summary_response.choices[0].message.content.strip())
