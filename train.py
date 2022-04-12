import click
import os
import torch
from torch.utils.data import DataLoader
import logging

from src.models.decoder import TextDecoder
from src.models.encoder import ImageEncoder
from scripts.utils.dataset_utils import CustomCircuitDataset


@click.command()
@click.option(
    "--data_dir",
    default="data",
    help="Path to the directory containing the images and formulas.",
)
@click.option(
    "--images_folder",
    default="circuit_images",
    help="Name of the directory inside the data one, containing the images.",
)
@click.option(
    "--circuit_metadata_files",
    default="circuit2latex.lst",
    help="Name of the file containing the circuit metadata.",
)
@click.option(
    "--formulas_file_name",
    default="circuitikz_code.lst",
    help="Name of the file containing the circuit formulas.",
)
@click.option(
    "--n_epochs",
    default=2,
    help="Number of epochs for the training.",
)
def main(
    data_dir: str,
    images_folder: str,
    circuit_metadata_files: str,
    formulas_file_name: str,
    n_epochs: int = 10,
    learning_rate: float = 0.005,
) -> None:

    # create vocabulary & load data
    data = CustomCircuitDataset(
        os.path.join(data_dir, circuit_metadata_files),
        os.path.join(data_dir, formulas_file_name),
        os.path.join(data_dir, images_folder),
    )
    dataloader = DataLoader(data, batch_size=64, shuffle=True)
    ds_size = len(dataloader.dataset)

    # check if cuda is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logging.info(f"Using {device} device")

    # instanciate the models
    encoder = ImageEncoder(ouptut_size=len(data.vocab)).to(device)
    logging.info(encoder)
    # output size of the encoder : vocabulary size
    decoder = TextDecoder(data.vocab).to(device)
    logging.info(decoder)

    optimizer = torch.optim.Adam(
        [{"params": encoder.parameters()}, {"params": decoder.parameters()}],
        lr=learning_rate,
    )
    loss_ftn = torch.nn.CrossEntropyLoss()  # for now, we use cross entropy loss

    for epoch in range(n_epochs):
        print(f"Epoch {epoch}")
        for batch, (X, y) in enumerate(dataloader):
            # Compute prediction and loss
            pred = decoder(encoder(X))
            loss = loss_ftn(pred, y)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch % 1 == 0:
                loss, current = loss.item(), batch * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{ds_size:>5d}]")

    # save the trained models
    torch.save(encoder, os.path.join("trained_models", "encoder.pt"))
    torch.save(decoder, os.path.join("trained_models", "decoder.pt"))

    # get one batch of data
    # train_features, train_labels = next(iter(dataloader))
    # enc_output = encoder(train_features)
    # dec_output = decoder(enc_output)
    # print(dec_output)

    # label = train_labels[0]
    # plt.imshow(img, cmap="gray")
    # plt.show()
    # print(f"Label: {label}")
    # encoder = ImageEncoder()
    # decoder = Decoder(input_dim=10, vocab_size=10)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
