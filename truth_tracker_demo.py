import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from openai import OpenAI
import json
import os
from key import API_KEY

# Set up Model.
client = OpenAI(api_key=API_KEY)

# target_classifier = AutoModelForCausalLM.from_pretrained(
#     "gpt2",
#     torch_dtype="auto",
#     trust_remote_code=True,
# )

# bias_classifier = AutoModelForCausalLM.from_pretrained(
#     "gpt2",
#     torch_dtype="auto",
#     trust_remote_code=True,
# )

# tokenizer = AutoTokenizer.from_pretrained("gpt2")

# target_pipe = pipeline(
#     "text-generation",
#     model=target_classifier,
#     tokenizer=tokenizer,
# )

# bias_pipe = pipeline(
#     "text-generation",
#     model=bias_classifier,
#     tokenizer=tokenizer,
# )


def display_article_with_bias(article_text):
    biased_sentences = identify_biased_sentences(article_text)
    paragraphs = article_text.split("\n")
    displayed_sentences = []

    for i, p in enumerate(paragraphs):
        displayed_paragraph = []
        for j, sentence in enumerate(p.split(".")):
            if sentence in (" ", ""):
                continue
            sentence += "."
            try:
                bias_pred = biased_sentences[i][j]
            except:
                continue
            if bias_pred["biased"]:
                # Display the biased sentence with a class for tooltip
                # st.markdown(f'<span class="tooltip">{sentence.strip()}<span class="tooltiptext">This sentence is biased with 90% confidence</span></span>', unsafe_allow_html=True)
                # displayed_paragraph.append(f"<p class='sentence'>{sentence}</p>")
                displayed_paragraph.append(
                    f"<span class='tooltip sentence'>{sentence}<span class='tooltiptext'>Target: {bias_pred['target']}, Reason: {bias_pred['reason']}</span></span>"
                )
            else:
                # st.write(sentence.strip())
                displayed_paragraph.append(sentence)
        displayed_sentences.append("\n".join(displayed_paragraph))

    st.markdown(" ".join(displayed_sentences), unsafe_allow_html=True)


def identify_biased_sentences(article_txt):
    # Placeholder function to identify biased sentences
    # Replace this with your actual bias detection logic
    paragraphs = article_txt.split("\n")
    predictions = []
    for paragraph in paragraphs:
        prompt = " ".join(
            [
                "For every sentence of the following article, identify whether the sentence is biased. If the sentence is biased, give a short",
                "sentence on why the sentence is biased as well as the target the bias is directed to. If the sentence is not biased,"
                "simply return None. Output one json for every sentence, and every json is separated by a semi-colon ;/ Here is an example:"
                "Input article: The new government policy unfairly favors wealthy corporations while neglecting the needs of small businesses.",
                "The new government policy has received mixed reactions, with some expressing concerns about its potential impact on small businesses."
                "Output:",
                '{"biased" : true, "reason" : "The sentence presents a subjective viewpoint without considering opposing perspectives or providing',
                'evidence to support its claim.", "target" : "the wealthy corporation"};',
                '{"biased" : false, "reason" : null, "target" : null}',
                f"Here is the article. It has {len(paragraph.split('.'))} sentences:",
                f"{paragraph}",
            ]
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a media bias detector that classifies which sentences are biased and for what reason.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        preds = []

        result = completion.choices[0].message.content.split(";")
        for r in result:
            try:
                with open("temp.json", "w") as f:
                    f.write(r)
                    f.close()
                with open("temp.json", "r") as f:
                    preds.append(json.load(f))
            except:
                continue
        predictions.append(preds)

    return predictions


# Main code
def main():
    st.title("Article Bias Detection Demo")

    # Sample article text

    option = st.selectbox("Select an option:", ("Huffington Post", "Fox", "NY Times"))

    article_dict = {
        "Huffington Post": "2f3e86b6-8443-47bd-9cd3-491c90a59fe9_1.json",
        "Fox": "2f3e86b6-8443-47bd-9cd3-491c90a59fe9_2.json",
        "NY Times": "2f3e86b6-8443-47bd-9cd3-491c90a59fe9_3.json",
    }

    articles_dir = "BASIL/articles"
    year = "2019"
    filename = article_dict[option]
    article = json.load(open(os.path.join(articles_dir, year, filename), "r"))

    article_text = [" ".join(paragraph) for paragraph in article["body-paragraphs"]]
    article_text = "\n".join(article_text)
    st.header(article["title"])

    # Display the article with bias detection
    display_article_with_bias(article_text)

    # Custom CSS for tooltip
    st.markdown(
        """
        <style>
        .sentence {
            background-color: #fffd77b3;
            padding: 3px;
        }

        .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
        }

        .tooltip .tooltiptext {
        visibility: hidden;
        width: 220px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -110px;
        opacity: 0;
        transition: opacity 0.3s;
        }

        .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
