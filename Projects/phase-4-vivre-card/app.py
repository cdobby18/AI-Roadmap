"""
Gradio UI for Vivre Card semantic character search.
Run embeddings.py first, then: python app.py
"""

import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModel
from search import load_index, search


print("Loading index...")
embeddings, characters, model_name = load_index()

print(f"Loading {model_name}...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()

EXAMPLES = [
    "a rubber man who wants to become king of the pirates",
    "a swordsman obsessed with becoming the world's greatest",
    "someone who can freeze the sea and is relaxed and easygoing",
    "a blind admiral who controls gravitational force",
    "a doctor who transforms between animal and human forms",
    "a living skeleton who plays music and uses ice powers from his soul",
    "someone who creates earthquakes and calls every pirate their child",
    "a cook who fights only with kicks and dreams of an ocean with all fish",
    "a crime lord who controls sand and crumbles everything he touches",
    "a navigator who can read and control the weather",
]


def run_search(query, top_k):
    if not query.strip():
        return "Enter a description to search."

    results = search(query, embeddings, characters, tokenizer, model, top_k=int(top_k))

    output = ""
    for i, r in enumerate(results, 1):
        bar_len = int(r["score"] * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        output += f"### {i}. {r['name']}  ·  *{r['role']}*\n"
        output += f"`{bar}` **{r['score']:.1%}** match\n\n"
        output += f"{r['bio']}\n\n---\n\n"
    return output


with gr.Blocks(title="Vivre Card — One Piece Semantic Search") as demo:
    gr.Markdown(
        """
# Vivre Card
### One Piece Character Semantic Search

Describe a character in your own words. BERT will find the best match by meaning — not keyword.
"""
    )

    with gr.Row():
        with gr.Column(scale=3):
            query_box = gr.Textbox(
                label="Describe a character",
                placeholder="e.g. a fire user who is the adopted brother of the captain",
                lines=2,
            )
        with gr.Column(scale=1):
            top_k_slider = gr.Slider(
                minimum=1, maximum=10, value=3, step=1, label="Results to show"
            )

    search_btn = gr.Button("Search", variant="primary")
    results_box = gr.Markdown(label="Results")

    gr.Examples(
        examples=EXAMPLES,
        inputs=query_box,
        label="Try these queries",
    )

    search_btn.click(fn=run_search, inputs=[query_box, top_k_slider], outputs=results_box)
    query_box.submit(fn=run_search, inputs=[query_box, top_k_slider], outputs=results_box)

demo.launch()
