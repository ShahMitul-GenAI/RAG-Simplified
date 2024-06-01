# RAG Simplified

This project provides a practical demonstration of Retrieval-Augmented Generation (RAG) technology in an accessible manner. It empowers users to explore comprehensive answers to their queries by leveraging either Wikipedia or a dedicated research paper tailored to RAG.

### Features
- Users can choose between `Wikipedia` or `Research Paper` as the source of information.
- Information retrieval from Wikipedia is dynamic and can be updated with the latest content.
- The `Research Paper` option provides information specifically about RAG.

## Setup

### Installation
1. Clone this repository to your local machine:
```bash
git clone https://github.com/ShahMitul-GenAI/RAG-Simplified
```

2. Navigate to the project directory:
```bash
cd simplified_rag
```

3. Install Poetry using pip (if not already installed):
```bash
pip install poetry
```

4. Activate the virtual environment created by Poetry:
```bash
poetry shell
```

5. Install project dependencies using Poetry:
```bash
poetry install
```

6. Create a `.env` file and add your own OpenAI API key in the `.env` file as follows:
```
OPENAI_API_KEY=your-key-here
```

by replacing `xxxxxxxx` with your own key. 

### Running the Application
1. After installing the dependencies, you can run the Streamlit app by executing the following command:
```bash
streamlit run app.py
```

2. Once the server starts, open a web browser and follow the link displayed by Streamlit to access the application.

### Usage
1. Upon launching the application, you'll be presented with a dropdown menu to select the information source: either `Wikipedia` or `Research Paper`.

2. Choose the desired source, and the app will retrieve relevant information based on your selection.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
