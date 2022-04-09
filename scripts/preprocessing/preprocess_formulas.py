from typing import List, Tuple
import re
import torch
import torch.nn.functional as F
import logging


class Vocabulary:
    def __init__(self, freq_threshold: float = 0) -> None:
        self.freq_threshold = freq_threshold
        self.formula_max_length = None
        self.idx_to_word = {0: "<PAD>", 1: "<SOS>", 2: "<EOS>", 3: "<UNK>"}
        self.word_to_idx = {word: idx for idx, word in self.idx_to_word.items()}
        # default tensor data type used for the formulas
        self.dtype: torch.dtype = torch.int64  # uint8 cannot be used to one hot encode

    def __len__(self) -> int:
        return len(self.word_to_idx)

    def build_vocaulary(self, file_path: str) -> None:
        """From a text file containing formulas, tokenize them and return a list of tokens + UNK, PAD, EOS, SOS...
        Saves the:
            The list of possible tokens
            A maximal length for formulas
        """
        # read the formulas
        with open(file_path, "r") as f:
            formulas = f.readlines()
        tokens = set()
        # find the maximum length of the formulas
        max_length = 0
        # if we find new tokens in that formula, add them to the set
        for formula in formulas:
            tokenized_formula = self.basic_tokenize(formula)
            tokens.update(tokenized_formula)
            if len(tokenized_formula) > max_length:
                max_length = len(tokenized_formula)

        self.formula_max_length = max_length + 2  # +2 for SOS and EOS
        # if the indexes cannot be represented with an
        if self.formula_max_length > 255:
            logging.info("Using uint16 as torch.tensor dtype.")
            # max value : 32767
            self.dtype = torch.int16

        # add the tokens to the vocabulary
        for token in sorted(list(tokens)):
            idx = len(self.word_to_idx)
            self.word_to_idx[token] = idx
            self.idx_to_word[idx] = token

    def basic_tokenize(self, formula: str) -> List[str]:
        """Returns a list of tokens corresponding to the input formula.
        This basic version splits formulas on spaces. Those formulas are generated accordingly.
        (later) : check if the token is in the vocabulary and use <UNK> if not.
        """
        return re.findall(r"to\[[\w\s]+\]|[a-z0-9\\]+|\([0-9|\s,]+\)|;", formula)

    def pad(self, tokens_list: List[str]) -> List[str]:
        """Pads the tokens list with <PAD> tokens to make them formula_max_length"""
        nb_pads = self.formula_max_length - len(tokens_list) - 2
        return ["<SOS>"] + tokens_list + ["<EOS>"] + ["<PAD>"] * nb_pads

    def numericalize(self, tokens_list: List[str]) -> torch.Tensor:
        """Convert the list of words to a tensor of indices"""
        return torch.tensor(
            tuple(self.word_to_idx[word] for word in tokens_list), dtype=self.dtype
        )

    def one_hot_encode(self, numeric_tokens_list: torch.Tensor) -> torch.Tensor:
        """Convert the list of words to a one hot encoded tensor"""
        return F.one_hot(numeric_tokens_list, num_classes=len(self))

    def preprocess_formula(self, formula: str) -> torch.Tensor:
        """Processes the latex formula to be used to train a model.
        tokenizes, then pads, then converts it into a vector
        """
        tokens = self.basic_tokenize(formula)
        padded_formula = self.pad(tokens)
        num_formula = self.numericalize(padded_formula)
        encoded_tokens_formula = self.one_hot_encode(num_formula)
        return encoded_tokens_formula

    def get_encoded_token(self, str_token: str) -> torch.Tensor:
        """Returns the one hot encoded vector corresponding to a single token

        e.g. get_encoded_token('<PAD>') = tensor([1., 0., ..., 0.])
        """
        num_token = self.numericalize([str_token])
        encoded_token = self.one_hot_encode(num_token)
        return encoded_token.squeeze()
