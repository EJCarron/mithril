import hashlib


def generate_node_id(original_node_identifier, node_type_str):
    unique_node_string = f'{original_node_identifier}_{node_type_str}'

    sha256_hash = hashlib.sha256()

    # Convert the input string to bytes and add it to the hash object
    sha256_hash.update(unique_node_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    unique_id = sha256_hash.hexdigest()

    return unique_id
