## MSF-Agents

LLM + Agents + Langchain + MSF API + Neo4J KB + Streamlit - A hobby project with the learning of LLM Agents with a Knowledge graph.

- Requires a Marvel Strike Force Web account to authenticate
- A Neo4J Knowledge graph connection to store the data.

### Installation

Requires python >= 3.11, Neo4J credentials, OpenAI API key and MSF account.

- Install libraries via ```pip install -r requirements.txt```
- Then add the .env variable as in ```.env.example```
- A client ID for your own app at MSF
- X-API-KEY available from the [MSF Dev Portal](https://developer.marvelstrikeforce.com/beta/index.html)

### Usage

- Run ```streamlit run app.py```
- Authenticate first time and paste the redirected URL on the small text input
- Once data loading completed, start querying!

### TODO:
- RAG on descriptive data
- More guided usecases on streamlit
- Integrate other Cypher queries into tools
- Extended API search
- web crawl (optional) -> future feature
