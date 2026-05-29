"""
Gradio — wrap any model in a shareable UI in under 10 lines.
Run: pip install gradio
Then: python 03-gradio-demo.py  →  opens at http://127.0.0.1:7860
"""
import gradio as gr
from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def predict_sentiment(text):
    result = classifier(text)[0]
    return f"{result['label']} ({result['score']:.2%})"

demo = gr.Interface(
    fn=predict_sentiment,
    inputs=gr.Textbox(label="Enter text"),
    outputs=gr.Textbox(label="Sentiment"),
    title="Sentiment Classifier",
    description="Powered by a pre-trained Hugging Face model.",
)

demo.launch()
