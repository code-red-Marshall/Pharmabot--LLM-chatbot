# # Pharmabot : A natural Responsive Chatbot made using Google PaLM 2

![google_palm2_hero_1](https://github.com/code-red-Marshall/Pharmabot--LLM-chatbot/assets/82904501/6f377da5-54ec-444e-982d-3136664b49c9)


This repository contains the code for a bot that can answer questions about drug pricing based on a given composition, strength, and dosage.


## Files in the Repository

- `main.py`: The main Python script that executes the core functionalities of this project.
- `preprocessing.py`: A Python script used for cleaning and preparing the final database.
- `data.csv`: The final data that is converted to embeddings using huggingface embeddings (model_name='sentence-transformers/all-MiniLM-L6-v2').
- `new_NLEM_cellingprice.csv`: Database containing specific data on the ceiling prices of drugs listed under NLEM (National List of Essential Medicines).
- `pharmatrack_non-scheduled.csv`: Database with data related to non-scheduled pharmaceutical drugs and their tracking information.

## Business Problem: 
Developing a medical chatbot to categorize medicines and devices, including new and scheduled/non-scheduled classifications.
## Business Success Criteria :
Increase customer engagement on the website by 30%
## Economic Success Criteria :
Increased customer engagement on the website, contributing to an approximate annual revenue growth of $20,000 in the healthcare sector.


## Chatbot Architecture: 

![sda (1)](https://github.com/code-red-Marshall/Pharmabot--LLM-chatbot/assets/82904501/cd47adc9-68cb-4ee3-9159-8aa12a2aba2f)

## Bot Flow:

Step 1 : The user puts in the details of the drug i.e Composition + Strength + Dosage and asks if the combination is Scheduled or Non-Scheduled
Step 2 : The bot checks if the combination is available in the dataset. 
It then fetches the information from the given dataset and comes back with the answer : Scheduled/Non-scheduled/ New Drug.
Step 3: If the drug is not found in the dataset, it will be considered as a new drug directly. And the bot asks the user to contact the team for further pricing details.

Step 4:  if the drug is non-scheduled, the bot first asks if the manufacturer is an existing producer of the drug before may 2013. If yes, that drug will be considered as a new drug. If no, the bot identifies the drug as a non-scheduled drugs. 

Step 5: If the drug is Scheduled, the bot identifies the drug as Scheduled drugs. 

Step 6: The bot also asks if the user wants to know the MRP of the combination.
If non-scheduled : The MRP for the present year is mentioned in the dataset and the bot fetches it from the vector database. The MRP of non-scheduled drugs can be increased by 10% every 12 months from the date of last updated price.
if Scheduled : The formulation of MRP for scheduled drugs is : Ceiling Price * Pack unit * GST%
if New Drugs :  Contact team for further pricing details.


## Setup

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install all dependencies listed in `requirements.txt` using `pip install -r requirements.txt`.
4. Run the main.py to initiate the bot and start asking queries for the formulations present in the csv file named "data"

## Usage

1. Ensure all required data files (`data.csv`, `new_NLEM_cellingprice.csv`, `pharmatrack_non-scheduled.csv`) are present in the project directory.
2. Run `preprocessing.py` to clean and prepare your data.
3. Execute `main.py` to perform core operations and obtain results/output based on provided datasets.

## Contributing

Feel free to fork this repository, make changes or improvements, and create pull requests. We appreciate your contributions!
