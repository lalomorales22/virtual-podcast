# Virtual Podcast App
<img width="1243" alt="Screenshot 2024-08-19 at 9 19 36 AM" src="https://github.com/user-attachments/assets/9385064a-2987-4ca9-8f28-abb3b6a72204">

## Overview

The Virtual Podcast App is a Streamlit-based web application that generates AI-powered podcast-style conversations. Users can set up multiple AI guests, define a topic, and watch as the app creates a dynamic, multi-round discussion between these virtual participants.

## Features

- Support for multiple AI language models (OpenAI and Ollama)
- Customizable number of podcast guests (2-5)
- Ability to define guest backgrounds and expertise
- User-defined podcast topic and number of conversation rounds
- Real-time streaming of AI-generated responses
- Save and load podcast conversations
- Token usage tracking

## Requirements

- Python 3.7+
- streamlit
- openai
- ollama
- python-dateutil
- requests
- pillow

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/virtual-podcast-app.git
   cd virtual-podcast-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the sidebar to configure your podcast:
   - Select an AI model
   - Set the number of guests (2-5)
   - Enter names and descriptions for each guest
   - Specify the podcast topic
   - Choose the number of conversation rounds

4. Click "Start Podcast" to generate the conversation.

5. Optionally, save the podcast conversation or load a previously saved one using the sidebar options.

## Saving and Loading Podcasts

- To save a podcast, enter a filename in the "Save podcast as:" field and click "Save Podcast".
- To load a podcast, use the file uploader in the sidebar, select the desired podcast from the dropdown, and click "Load Selected Podcast".

## Token Usage

The app tracks token usage for both prompts and completions. This information is displayed in the sidebar and can be useful for managing API costs or optimizing conversations.

## Customization

You can extend the app by adding more AI models to the `MODELS` list in the code. Additionally, you can modify the system prompts or add more features to enhance the podcast experience.

## Contributing

Contributions to improve the Virtual Podcast App are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is open-source and available under the MIT License.
