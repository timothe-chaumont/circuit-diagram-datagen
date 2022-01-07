
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


if __name__ == '__main__':
    # simple test
    import random as rd
    from os.path import dirname, abspath, join

    filepath = join(dirname(dirname(dirname(abspath(__file__)))), "tokens.lst")
    tokens_list = read_tokens(filepath)
    token_to_idx, idx_to_token = create_dictionnaries(tokens_list)

    random_seq = rd.sample(range(len(tokens_list)), 10)
    print([idx_to_token[i] for i in random_seq])
