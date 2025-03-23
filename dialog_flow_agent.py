from langchain_agent import get_pandas_agent_response,get_pandas_agent,pretty_print_response
from llm_helper import get_final_report,get_response_summary,intent_classifier
import os

def dialogue_mgmt_system():
    print("Welcome to your data analysis assistant!!")
    print("You can simulate a conversation with your data analysis assistant")
    print("You can ask questions about the dataset and get the analysis done")
    dataset_description = input("Enter the one word description of the dataset(eg loan, credit, insurance etc):")
    print("==================================================================")
    filename = input("Enter the filepath(csv) for the dataset:")
    if not os.path.exists(filename):
        print("File not found. Please enter the correct file path")
        return
    agent = get_pandas_agent(filename)
    print("==================================================================")
    print("Agent created for dataset:", filename)
    print("==================================================================")
    print("You can ask questions about the dataset and get the analysis done")
    print("==================================================================")
    dict = {}
    while(True):
        user_input = input("Enter your query or type 'exit' to end the conversation:")
        if (user_input == 'exit'):
            print("Thank you for using the Data Analysis Assistant!")
            if dict:
                print("Creating a detailed analysis report from your questions....")
                get_final_report(dict)
            break
        intent = intent_classifier(user_input, dataset_description)
        print("Intent of the query:",intent)
        if intent == "Not Applicable":
            print("The intent of the query could not be classified. Please ask a valid question")
            continue
        query = "You are a {intent} expert.Use all rows in the provided dataframe for the given question {user_input}"
        query = query.format(intent=intent,user_input=user_input)
        response = get_pandas_agent_response(agent, user_input)
        pretty_print_response(user_input, response)
        print("Brief summary of the response:")
        get_response_summary(user_input, response["output"])
        print("==================================================================")
        dict[user_input] = response["output"]
dialogue_mgmt_system()