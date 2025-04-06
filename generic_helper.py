# Author: Dhaval Patel. Codebasics YouTube Channel
#
# import re
#
# def get_str_from_food_dict(food_dict: dict):
#     result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
#     return result
#
#
# def extract_session_id(session_str: str):
#     print(f"Extracting session ID from: {session_str}")  # Debugging
#     match = re.search(r"/sessions/(.*?)/contexts/", session_str)
#     if match:
#         extracted_string = match.group(1)  # Changed to group(1) to extract the actual session ID
#         print(f"Extracted session ID: {extracted_string}")  # Debugging
#         return extracted_string
#
#     return ""
import re

def get_str_from_food_dict(food_dict: dict):
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result


def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        return match.group(1)  # Return only the session ID
    return ""