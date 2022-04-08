import os
import pandas as pd
from torchvision.io import read_image
from torch.utils.data import Dataset

from scripts.preprocessing.preprocess_formulas import Vocabulary


class CustomCircuitDataset(Dataset):
    LINE_INDEX = 0
    IMG_NAMES_INDEX = 1

    def __init__(self, annotations_file: str, formulas_file: str, img_dir: str, transform=None, target_transform=None):
        # read formula line, image name and version
        self.circuit_data = pd.read_csv(annotations_file, sep=' ', header=None)
        self.formulas = pd.read_csv(formulas_file, sep='#', header=None) # delimiter character # is not in the dataset
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        # create vocabulary
        self.vocab = Vocabulary()
        self.vocab.build_vocaulary(formulas_file)

    def __len__(self):
        """Returns the number of examples in the dataset."""
        return len(self.circuit_data)

    def __getitem__(self, idx):
        """Args:
            idx (int): Index of the example between 0 and nb_exambles - 1.
        """
        img_path = os.path.join(self.img_dir, 
            self.circuit_data.iloc[idx, self.IMG_NAMES_INDEX]) + ".jpg"
        image = read_image(img_path)
        formula_line = self.circuit_data.iloc[idx, self.LINE_INDEX]
        # read circuit formula
        formula_str = self.formulas.iloc[formula_line-1, 0]
        formula = self.vocab.preprocess_formula(formula_str)
        # apply possible transformations
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, formula
