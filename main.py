# Section 1: Import necessary libraries
import ast
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.llms import GooglePalm
from langchain.chains import RetrievalQA


# Section 2: Define constants
DB_FAISS_PATH = 'vectorstore/db_faiss'

# Section 3: Define functions
def create_vector_db():
    # Function to create vector database
    loader = CSVLoader("C:/Users/nathb/Downloads/new bot flow/data.csv")
    documents = loader.load()

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                   model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(documents, embeddings)
    db.save_local(DB_FAISS_PATH)

import tqdm as notebook_tqdm
create_vector_db()

custom_prompt_template = """Use the following pieces of information to answer the user's question - compositions, strength, dosage, NLEM 2022,
PTR, MRP, ceiling price. MRP is the price of a drug and PTR is the Price-to-Retailer of a drug. Based on these pieces of information, 
answer the questions asked by the user.If the user enters a composition that is neither scheduled nor non-scheduled, mention it as new drug.
If the composition includes multiple drugs separated by '+', consider it as a formulation for the composition. Also if the composition is not found in the database provided, do not create false information.
Respond back as "drug not found" in database.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    # Function to set custom prompt
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                        input_variables=['Input', 'Details'])
    return prompt
    
def retrieval_qa_chain(llm, prompt, db):
    # Function to create retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return qa_chain

api_key = 'AIzaSyCBLX_1uxkj9BbJEzhbTfi5oPSAp-9z_WI'

def load_llm():
    # Function to load language model
    llm = GooglePalm(google_api_key=api_key, temperature=0)
    return llm

def qa_bot():
    # Function to create QA bot
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                      model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa


def final_result(composition, strength, dosage, manufacturer=None, pack_size=None, gst=None):
    # Construct the query based on the composition, strength, and dosage
    query = f'Is {composition} {strength} {dosage} scheduled?'

    # Retrieve the drug info
    qa_result = qa_bot()
    response = qa_result({'query': query})

    # Extract the required information from the response
    page_content = response['source_documents'][0].page_content
    details = ast.literal_eval(page_content.split("Details: ")[1])[0]  # Parse the string into a Python object
    nlem_status = details.get('NLEM 2022', None)

    # Check if the drug is found in the database
    if nlem_status is None:
        if manufacturer == 'yes':
            return "This is a new drug. For further details, please contact our team.", 'New Drug'
        else:
            return "This is a non-scheduled drug. Contact team for pricing details.", 'Non-Scheduled'
    elif nlem_status == 'Non-Scheduled':
        mrp = details.get('MRP', 'N/A')
        ptr = details.get('PTR', 'N/A')
        if manufacturer == 'no':
            response = (f"The drug {composition} with strength {strength} and dosage {dosage} "
                        f"is a non-schedule formulation (as the API {composition} is not available in the NLEM. "
                        f"Its MRP is {mrp}. The MRP of non-scheduled drugs can be increased by 10% every 12 months from the date of last updated price.")
        elif manufacturer == 'yes':
            response = "This will be classified as 'new drug'. For further pricing details, please contact our team."
        return response, nlem_status
    else:
        ceiling_price = details.get('Ceiling_price', 'N/A')
        if pack_size is not None and gst is not None:
            c_mrp = float(ceiling_price) * pack_size * (1 + gst/100)
            return f"The MRP of {composition} is {c_mrp}.", nlem_status
        else:
            return f"The drug {composition} with strength {strength} and dosage {dosage} is scheduled under NLEM with a ceiling price of {ceiling_price}.", nlem_status



def interactive_bot():
    # Initialize the conversation state
    conversation_state = {
        'composition': None,
        'strength': None,
        'dosage': None,
        'manufacturer': None,
        'pack_size': None,
        'gst': None,
        'nlem_status': None,
        'want_mrp': None
    }

    # Start the conversation
    print('Please enter the name of the formulation:')
    
    while True:
        # Get user input
        query = input('Enter your query (or type "quit" to exit): ')

        # Check if the user wants to quit
        if query.lower() == 'quit':
            break

        # Check the state of the conversation to decide the next question
        if conversation_state['composition'] is None:
            conversation_state['composition'] = query
            print('Please provide strength?')
        elif conversation_state['strength'] is None:
            conversation_state['strength'] = query
            print('Please provide dosage?')
        elif conversation_state['dosage'] is None:
            conversation_state['dosage'] = query
            response, nlem_status = final_result(conversation_state['composition'], 
                                                 conversation_state['strength'], 
                                                 conversation_state['dosage'])
            print(response)
            conversation_state['nlem_status'] = nlem_status
            if nlem_status == 'Non-Scheduled':
                print('Did you manufacture any of the combination, before 2013?')
            elif nlem_status == 'New Drug' or nlem_status == 'Non-Scheduled':
                # Reset the conversation state for the next query
                conversation_state = {
                    'composition': None,
                    'strength': None,
                    'dosage': None,
                    'manufacturer': None,
                    'pack_size': None,
                    'gst': None,
                    'nlem_status': None,
                    'want_mrp': None
                }
                print('Please enter the name of the next formulation:')
            else:
                print('Do you want to know the MRP of the drug?')
        elif conversation_state['manufacturer'] is None and conversation_state['nlem_status'] == 'Non-Scheduled':
            conversation_state['manufacturer'] = query
            response, nlem_status = final_result(conversation_state['composition'], 
                                                 conversation_state['strength'], 
                                                 conversation_state['dosage'],
                                                 conversation_state['manufacturer'])
            print(response)
            # Reset the conversation state for the next query
            conversation_state = {
                'composition': None,
                'strength': None,
                'dosage': None,
                'manufacturer': None,
                'pack_size': None,
                'gst': None,
                'nlem_status': None,
                'want_mrp': None
            }
            print('Please enter the name of the next formulation:')
        elif conversation_state['want_mrp'] is None and conversation_state['nlem_status'] != 'Non-Scheduled':
            conversation_state['want_mrp'] = query.lower() == 'yes'
            if conversation_state['want_mrp']:
                print('Please provide the pack size:')
        elif conversation_state['pack_size'] is None and conversation_state['nlem_status'] != 'Non-Scheduled' and conversation_state['want_mrp']:
            conversation_state['pack_size'] = float(query)
            print('Please provide the GST percentage:')
        elif conversation_state['gst'] is None and conversation_state['nlem_status'] != 'Non-Scheduled' and conversation_state['want_mrp']:
            conversation_state['gst'] = float(query)
            response, nlem_status = final_result(conversation_state['composition'], 
                                                 conversation_state['strength'], 
                                                 conversation_state['dosage'],
                                                 conversation_state['manufacturer'],
                                                 conversation_state['pack_size'],
                                                 conversation_state['gst'])
            print(response)
            # Reset the conversation state for the next query
            conversation_state = {
                'composition': None,
                'strength': None,
                'dosage': None,
                'manufacturer': None,
                'pack_size': None,
                'gst': None,
                'nlem_status': None,
                'want_mrp': None
            }
            print('Please enter the name of the next formulation:')

    print("Goodbye!")

# Section 4: Run the bot
interactive_bot()