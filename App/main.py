import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import json
from App.predict import predict
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent  

# Build dataset path relative to project root
investment_dataset_path = (
    base_dir / "DataSets" / "Datasets_Investment" / "investment_dataset.csv"
)

print(f"Path is {investment_dataset_path}")
print("Exists:", investment_dataset_path.exists())


# Reading my dataSet here
def load_dataset(file_path):
    return pd.read_csv(file_path)



# For Converting each row to structured text(rows and columns)
def convert_rows(df):
    return df.apply(lambda row: (
        f"Name: {row['Name']}, "
        f"Age: {row['Age']}, "
        f"Investment Amount: {row['Investment_Amount']}, "
        f"Tenure: {row['Tenure']} years, "
        f"Risk Tolerance: {row['Risk_Tolerance']}, "
        f"Investment Type: {row['Investment_Type']}, "
        f"Return Amount: {row['Return_Amount']}, "
        f"Return Percentage: {row['Return_Percentage']}%"
    ), axis=1).tolist()



# Set up for Chroma and embed rows for storing data as chunks
def store_in_chroma(text_chunks, batch_size=1000):
    from math import ceil
    clean_chunks = [text for text in text_chunks if isinstance(text, str) and text.strip()]
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(clean_chunks)

    client = chromadb.Client()
    collection = client.get_or_create_collection(name="investment_data")

    # Batch added to avoid max batch size
    num_batches = ceil(len(clean_chunks) / batch_size)
    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size
        collection.add(
            documents=clean_chunks[start:end],
            embeddings=embeddings[start:end].tolist(),
            ids=[str(j) for j in range(start, min(end, len(clean_chunks)))]
        )

    return collection, model
# extracting relavant data from user query and embedded model
def get_relevant_data(user_query, collection, embed_model, k=3):
    query_embedding = embed_model.encode([user_query])[0].tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results['documents'][0]

def getUserDetails(name, age, investmentAmount, tenure, riskTolerance):
    # df = load_dataset(r"C:\Users\DhanushAppireddy\Documents\GenAI_20-04-25\GenAIExpt\DataSets\Datasets_Investment\investment_dataset.csv")
    df = load_dataset(investment_dataset_path)
    text_chunks = convert_rows(df)
    collection, embed_model = store_in_chroma(text_chunks)

    #Adding predictive XGBoostRegressor model for more accuracy
    expectedAmount, expectedPercentage = predict(age, investmentAmount, tenure, riskTolerance)
    # user input for user_profile
    user_profile = {
        "Name": {name},
        "Age": {age},
        "Investment_Amount": {investmentAmount},
        "Tenure": {tenure},
        "Risk_Tolerance": {riskTolerance},
    }

    user_query = f"Age: {user_profile['Age']}, Investment_Amount: {user_profile['Investment_Amount']}, Tenure: {user_profile['Tenure']}, Risk_Tolerance: {user_profile['Risk_Tolerance']}"

    # RAG Style data extraction for getting only relevant data for the user
    relevant_data = get_relevant_data(user_query, collection, embed_model)
    print("relevant_data!!!!!", relevant_data)

    # Investment Advice
    # advice = generate_advice(user_profile, examples)

    # with open("investment_advice_RAG.json", "w", encoding="utf-8") as f:
    #     json.dump(advice, f, indent=4)

    #print("Succes. Our Investment advice for you is Ready. saved to investment_advice_RAG.json")
    # print(advice)
    return (relevant_data, expectedAmount, expectedPercentage)