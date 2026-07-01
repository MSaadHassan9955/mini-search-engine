"""
generate_sample_pdfs.py
------------------------
Generates 5 sample PDF documents (on different topics) into the
sample_pdfs/ folder, so you have a ready-made dataset to test the
Mini Search Engine with.

Usage:
    python generate_sample_pdfs.py
"""

import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_pdfs")

DOCUMENTS = {
    "artificial_intelligence.pdf": {
        "title": "An Introduction to Artificial Intelligence",
        "paragraphs": [
            "Artificial Intelligence (AI) refers to the simulation of human intelligence "
            "processes by computer systems. These processes include learning, reasoning, "
            "problem-solving, perception, and language understanding. AI has evolved from a "
            "purely academic research field into one of the most influential forces shaping "
            "modern technology, business, and daily life.",
            "Machine learning, a subset of AI, enables systems to learn patterns from data "
            "rather than being explicitly programmed with rules. Deep learning, which uses "
            "neural networks with many layers, has driven major breakthroughs in image "
            "recognition, natural language processing, and speech synthesis over the past decade.",
            "Vector embeddings are a core building block of modern AI systems. An embedding "
            "converts text, images, or other data into a numerical vector such that "
            "semantically similar items are located close to each other in vector space. "
            "This property is what makes semantic search possible: a search engine can find "
            "documents that are conceptually related to a query, even if they do not share "
            "the exact same keywords.",
            "Vector databases, such as Pinecone, are specialized systems designed to store and "
            "efficiently search over millions or billions of these embedding vectors. They use "
            "approximate nearest neighbor algorithms to quickly retrieve the most similar "
            "vectors to a given query, enabling real-time semantic search applications.",
            "As AI continues to advance, researchers are increasingly focused on making systems "
            "more transparent, fair, and aligned with human values. Responsible AI development "
            "requires careful attention to data quality, bias mitigation, privacy, and the "
            "broader societal impact of automated decision-making.",
        ],
    },
    "space_exploration.pdf": {
        "title": "The History and Future of Space Exploration",
        "paragraphs": [
            "Space exploration began in earnest during the mid-twentieth century, driven "
            "largely by the geopolitical rivalry between the United States and the Soviet "
            "Union. The launch of Sputnik 1 in 1957 marked the beginning of the Space Age and "
            "triggered a rapid acceleration in rocket and satellite technology.",
            "The Apollo program achieved one of humanity's most remarkable feats when Apollo 11 "
            "landed astronauts Neil Armstrong and Buzz Aldrin on the surface of the Moon in "
            "1969. This mission demonstrated that crewed missions beyond low Earth orbit were "
            "technically feasible and captured the imagination of people around the world.",
            "In recent decades, space exploration has shifted toward robotic missions, "
            "international collaboration, and increasingly, private industry involvement. "
            "Rovers such as Curiosity and Perseverance have explored the surface of Mars, "
            "searching for evidence of past microbial life and characterizing the planet's "
            "geology and climate history.",
            "Commercial space companies have dramatically reduced the cost of access to orbit "
            "through reusable rocket technology. This has opened new possibilities for "
            "satellite constellations, space tourism, and ambitious future missions to the "
            "Moon and Mars.",
            "Looking ahead, space agencies and private companies are planning sustained human "
            "presence on the Moon as a stepping stone toward crewed missions to Mars. These "
            "efforts will require advances in life support systems, radiation protection, and "
            "in-situ resource utilization to make long-duration deep space missions viable.",
        ],
    },
    "human_health.pdf": {
        "title": "Fundamentals of Human Health and Wellness",
        "paragraphs": [
            "Human health is a complex interplay of physical, mental, and social well-being, "
            "not merely the absence of disease. Maintaining good health requires attention to "
            "nutrition, physical activity, sleep, stress management, and social connection.",
            "Regular physical exercise has been shown to reduce the risk of chronic diseases "
            "such as cardiovascular disease, type 2 diabetes, and certain cancers. Exercise also "
            "improves mood, cognitive function, and overall quality of life by promoting the "
            "release of endorphins and supporting healthy brain function.",
            "A balanced diet rich in fruits, vegetables, whole grains, and lean proteins "
            "provides the essential nutrients the body needs to function properly. Poor "
            "nutrition is strongly linked to obesity, metabolic disorders, and reduced immune "
            "function, making dietary choices a cornerstone of preventive healthcare.",
            "Sleep plays a critical role in physical recovery, memory consolidation, and "
            "emotional regulation. Chronic sleep deprivation has been associated with impaired "
            "cognitive performance, weakened immunity, and increased risk of mental health "
            "conditions such as anxiety and depression.",
            "Mental health is increasingly recognized as being just as important as physical "
            "health. Practices such as mindfulness, regular social interaction, and access to "
            "mental health support services can significantly improve resilience to stress and "
            "overall life satisfaction.",
        ],
    },
    "personal_finance.pdf": {
        "title": "Principles of Personal Finance",
        "paragraphs": [
            "Personal finance encompasses the management of an individual's or household's "
            "financial activities, including budgeting, saving, investing, and planning for "
            "retirement. A solid understanding of personal finance principles can help people "
            "achieve financial security and long-term goals.",
            "Budgeting is the foundation of financial health. By tracking income and expenses, "
            "individuals can identify spending patterns, avoid unnecessary debt, and allocate "
            "resources toward savings and investment goals. The widely used 50/30/20 rule "
            "suggests allocating 50% of income to needs, 30% to wants, and 20% to savings.",
            "Building an emergency fund that covers three to six months of living expenses "
            "provides a financial safety net against unexpected events such as job loss or "
            "medical emergencies. This fund should be kept in a liquid, easily accessible "
            "account rather than invested in volatile assets.",
            "Investing allows money to grow over time through the power of compound interest. "
            "Diversifying investments across asset classes such as stocks, bonds, and real "
            "estate can help manage risk while pursuing long-term growth. Starting to invest "
            "early, even with small amounts, can have a substantial impact due to compounding.",
            "Retirement planning involves estimating future income needs and systematically "
            "saving through vehicles such as employer-sponsored retirement accounts or "
            "individual retirement accounts. Understanding tax implications and employer "
            "matching contributions can significantly improve long-term retirement outcomes.",
        ],
    },
    "ancient_civilizations.pdf": {
        "title": "Overview of Ancient Civilizations",
        "paragraphs": [
            "Ancient civilizations laid the foundations for many aspects of modern society, "
            "including systems of writing, law, governance, and architecture. Studying these "
            "early societies provides insight into the origins of human culture and social "
            "organization.",
            "The civilization of ancient Mesopotamia, located between the Tigris and Euphrates "
            "rivers, is often credited with developing one of the earliest writing systems, "
            "cuneiform, along with early codes of law such as the Code of Hammurabi, which "
            "established formalized rules for justice and society.",
            "Ancient Egypt flourished along the Nile River for thousands of years, developing "
            "sophisticated systems of agriculture, monumental architecture such as the "
            "pyramids, and a complex religious belief system centered on the afterlife. "
            "Egyptian hieroglyphics represent one of the world's oldest writing systems.",
            "In ancient Greece, city-states such as Athens pioneered concepts of democracy, "
            "philosophy, and scientific inquiry that continue to influence Western thought. "
            "Greek philosophers such as Socrates, Plato, and Aristotle explored fundamental "
            "questions about ethics, knowledge, and the natural world.",
            "The Roman Empire built upon Greek foundations to create an extensive system of "
            "law, engineering, and governance that spanned three continents at its height. "
            "Roman innovations in infrastructure, such as roads, aqueducts, and concrete "
            "construction, had a lasting impact on architecture and urban planning.",
        ],
    },
}


def build_pdf(filepath: str, title: str, paragraphs):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=20, spaceAfter=20
    )
    body_style = ParagraphStyle(
        "BodyStyle", parent=styles["BodyText"], fontSize=11, leading=16, spaceAfter=14
    )

    doc = SimpleDocTemplate(
        filepath,
        pagesize=LETTER,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    story = [Paragraph(title, title_style), Spacer(1, 12)]
    for para in paragraphs:
        story.append(Paragraph(para, body_style))
        story.append(Spacer(1, 6))

    doc.build(story)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename, content in DOCUMENTS.items():
        filepath = os.path.join(OUTPUT_DIR, filename)
        build_pdf(filepath, content["title"], content["paragraphs"])
        print(f"Created {filepath}")

    print(f"\nGenerated {len(DOCUMENTS)} sample PDFs in '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    main()
