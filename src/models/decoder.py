import torch
import torch.nn as nn
import torch.nn.functional as F

from scripts.preprocessing.preprocess_formulas import Vocabulary


class TextDecoder(nn.Module):
    def __init__(self, vocab: Vocabulary) -> None:
        """
        Args:
            vocab : (we can get vocab size, convert text tokens to OHE...)
            # formula_max_len (int) : maximal size of a formula
            # hidden_size : nb features (size) in the hidden state (= output)
        """
        super().__init__()
        self.vocab = vocab
        self.vocab_size = len(vocab)
        self.formula_max_len = vocab.formula_max_length

        self.lstm_cell = nn.LSTMCell(input_size=len(vocab), hidden_size=len(vocab))
        self.softmax = nn.Softmax(dim=-1)
        # later : add an embedding layer

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x (torch.Tensor): is a tensor of shape (batch_size, input_size)

        Returns:
            torch.Tensor: The tensor of one hot encoded tokens, generated by the decoder
        """
        batch_size = x.shape[0]

        # get SOS, EOS & PAD one-hot encoded vectors
        eos_vect_id = self.vocab.word_to_idx["<EOS>"]
        pad_vect = self.vocab.get_encoded_token("<PAD>")
        sos_vect = self.vocab.get_encoded_token("<SOS>")

        # will contain the probabilities for each prediction of the different tokens
        # initialized with <PAD> token One Hot Encoded (and <SOS> for the first token)
        predictions = (
            torch.ones(size=(batch_size, self.formula_max_len, self.vocab_size))
            * pad_vect
        )
        predictions[:, 0] = sos_vect

        # initialize hidden state with the encoder outputed vector <SOS> token
        hidden_state = x.squeeze()
        cell_state = torch.zeros_like(hidden_state)  # how to initialize it properly ?
        # initialize the input vector with the <SOS> token
        # shape (batch size, vocab_size)
        input_vect = torch.ones(size=(batch_size, self.vocab_size)) * sos_vect.to(
            torch.float32
        )

        # until the full formula has been predicted,
        for i in range(self.formula_max_len - 1):
            # run once through the LSTM
            hidden_state, cell_state = self.lstm_cell(
                input_vect, (hidden_state, cell_state)
            )
            pred_probas = self.softmax(hidden_state)
            pred_tokens = pred_probas.argmax(dim=1)
            predictions[:, i, :] = pred_probas

            # if the complete formula has been predicted, stop
            # if pred_token == eos_vect_id:
            #     break

            # update the input to be the predicted token
            input_vect = self.vocab.get_encoded_token(pred_tokens)

        return predictions
