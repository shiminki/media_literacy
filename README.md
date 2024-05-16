# Media Literacy Bias Detector

This project is a demo for detecting and analyzing political bias at the sentence level in news articles. The demo leverages OpenAI's GPT technology and is implemented using Streamlit for an interactive user interface. The data source for this demo is derived from the [BASIL dataset](https://github.com/launchnlp/BASIL/tree/main).

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Data Source](#data-source)

## Features

- **Sentence-Level Bias Detection**: Analyzes individual sentences for political bias.
- **Interactive Interface**: Uses Streamlit for a user-friendly experience.
- **Real-time Analysis**: Provides instant feedback on the bias present in the text.

## Usage

1. **Set Up Your OpenAI API Key**:
   Open `truth_tracker_demo.py` and replace `YOUR_OPENAI_API_KEY` with your actual OpenAI API key.

2. **Run the Application**:
   Use the following command to start the Streamlit application:

   ```bash
   streamlit run truth_tracker_demo.py
   ```

3. **Interact with the Demo**:
   Select the article source from the demo to get a real-time bias detection

## Data Source

The data for this demo is sourced from the [BASIL dataset](https://github.com/launchnlp/BASIL/tree/main), which contains annotated news articles for bias detection research.

## How It Works

1. **Input**: Users input a news article or specific sentences.
2. **Processing**: The text is processed using OpenAI's API to detect bias.
3. **Output**: The results are displayed on the Streamlit interface, highlighting sentences with detected bias.

---

Feel free to reach out with any questions or feedback! Happy bias detecting!
