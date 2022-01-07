
def read_tokens(filename="tokens.lst"):
    """Returns a list of all tokens corresponding
       duplicates will be removed.
    """
    with open(filename, "r") as f:
        data = [l.replace("\n", "").strip() for l in f.readlines()]
    return data


def create_dictionnaries(tokens):
    """Returns two dictionnaries of all tokens and their
       corresponding index.
    """
    token_to_idx = {t: i for i, t in enumerate(tokens)}
    idx_to_token = {i: t for i, t in enumerate(tokens)}
    return token_to_idx, idx_to_token
