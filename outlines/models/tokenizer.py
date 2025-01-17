from abc import abstractmethod
from typing import List, Protocol, Tuple, Union

import numpy as np
from numpy.typing import NDArray


class Tokenizer(Protocol):
    eos_token: str
    eos_token_id: int
    pad_token_id: int

    @abstractmethod
    def encode(
        self, prompt: Union[str, List[str]]
    ) -> Tuple[NDArray[np.int64], NDArray[np.int64]]:
        """Translate the input prompts into NumPy arrays of token ids and attention mask."""
        ...

    @abstractmethod
    def decode(self, token_ids: NDArray[np.int64]) -> List[str]:
        """Translate an array of token ids to a string or list of strings."""
        ...
