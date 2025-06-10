# Define the default prompt for the Llama model
prompt1 = """Classify the user's intent into one of the following categories and output only the intent name as a single word — no explanations, no labels:

1. Greet - For greetings like "hi", "hello", "how are you" etc.  
2. Status - For questions about the current status of a ticket.  
3. UnKnown - For anything else that does not fall under the above categories.

User Query: {query}

Only respond with one of: Greet, Status, UnKnown"""



prompt2 = """
if the user query has multiple questions, split the input query into multiple questions.

Understand the gist of the each input question and classify the user's intent into one of the following categories:

Classify the user's intent into one of the following categories and output one intent only as a single word like 'unknown' or 'greet' or 'status':

1. Greet - if user intent is to say like "hi", "hello", "how are you" etc.  
2. Status - if user intent is about knowing the status of a ticket or case number etc.  
3. UnKnown - if you are not sure or uncertain about the intent or mixed intents.

User Query: {query}

Intent:"""


RAG_PROMPT1 = """
step1:
Rephrase the question: include only the core ask and output the ask in a clear and appropriate 'how to' or 'what is' or 'why is' question. ONLY output the rephrased question.
Question: {query}

step2:
Label above rephrased question from a conversation with an intent. Reply ONLY with the name of the intent.

The intent should be one of the following:
- greet
- status
- unknown

Message: {query1}    # Got from vector database
Intent:  {intent1}   # Got from vector database
Message: {query2}    # Got from vector database
Intent:  {intent2}   # Got from vector database

Intent:

"""
