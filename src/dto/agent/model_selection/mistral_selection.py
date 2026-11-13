from enum import Enum


class MistralSelection(str, Enum):
    CODESTRAL = "codestral-latest"
    MISTRAL_SMALL = "mistral-small-latest"
    MISTRAL_NEMO = "open-mistral-nemo"

