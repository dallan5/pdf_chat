import tiktoken
def get_tokens(text, encoding_name = "cl100k_base"):
    #TODO: I can get the amount of tokens directly from the reponse message
    encoding = tiktoken.get_encoding(encoding_name)
    token_count = len(encoding.encode(str(text)))
    return token_count

def get_message_tokens(messages):
    tokens = 0
    for message in messages:
        tokens += get_tokens(message.get("content", ""))
    return tokens


def recursive_clear_messages(messages):
    # Remove messages intil tokens are less than 4990
    if not messages:
        return []

    tokens = get_message_tokens(messages)
    if tokens > 4990:
        #Always remove the index 2, since 0 and 1 are assistant instructions followed by text. Keep the rest
        messages = [item for i, item in enumerate(messages) if i != 2]
        return recursive_clear_messages(messages)
    else:
        return messages
