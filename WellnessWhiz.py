"""
Authorship Statement: I Jay Patel, 000881881 certify that this material is my original work. No other person's work has been used without due acknowledgement. I have not made my work available to anyone else.
Date: 15 March 2024
Description: A chatbot that provides information on diet, health, and wellness using OpenAI services.
"""

from builtins import print
from openai import OpenAI

# API key for OpenAI services
api_key = "--api key--"

# Creating a client object for accessing OpenAI services
client = OpenAI(api_key=api_key)

# History of conversation, initialized with a system role
history = [
    {"role": "system",
     "content": "You will be provided with questions, and your task is to answer them, only if it it related to diet, health and wellness, otherise DO NOT answer."}]


def generate_response(user_input):
    """
    Generate responses using two different models.

    Parameters:
        user_input (str): The input provided by the user.

    Returns:
        tuple: A tuple containing two responses generated by different models.
    """

    # First response using text completion API (Davinci model)
    response1 = client.completions.create(
        model="davinci-002", prompt=user_input, max_tokens=64, temperature=0.7
    )

    # Creating a dialog history for both user and system messages
    dialog = history + [{"role": "user", "content": user_input}]
    # Second response using chat API (GPT-3.5-turbo model)
    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=dialog, temperature=0.7, max_tokens=64
    )

    return response1.choices[0].text, response2.choices[0].message.content


def choose_best_response(response1, response2):
    """
    Choose the best response based on user feedback.

    Parameters:
        response1 (str): First response generated by a model.
        response2 (str): Second response generated by a different model.

    Returns:
        str: The selected best response.
    """
    # Creating a dialog history including current responses and asking for user preference
    dialog = history + [{"role": "system",
                         "content": "Which response is more informative, relevant, and helpful to the user based on the conversation history? only answer 'response 1' or 'response 2'\nConversation History:  \n"},
                        {"role": "user", "content": "\nResponse 1:\n"
                                                    + response1
                                                    + "\nResponse 2:\n"
                                                    + response2}]
    # Getting user's preference on the better response
    selection = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=dialog, temperature=0.7, max_tokens=10
    )

    # print(selection.choices[0].message.content.lower())

    # Checking user's choice and updating the conversation history accordingly
    if selection.choices[0].message.content.lower().__contains__("response 1"):
        history.append({"role": "system", "content": response1})
        return response1
    else:
        history.append({"role": "system", "content": response2})
        return response2


def main():
    """
    Main function to run the chatbot.
    """
    while True:
        # Taking user input
        user_input = input("User: ")

        # Exiting the conversation if user types 'exit'
        if user_input.lower() == "exit":
            break

        # Generating responses based on preprocessed user input
        response1, response2 = generate_response(user_input)

        # Choosing the best response based on user feedback
        best_response = choose_best_response(response1, response2)

        # Printing the best response
        print("WellnessWhiz:", best_response)


if __name__ == "__main__":
    # Starting message for the user
    print("Hello, I am a chatbot. I know stuff about diet, health and wellness. Type 'exit' to end the conversation.")

    # Starting the conversation loop
    main()
