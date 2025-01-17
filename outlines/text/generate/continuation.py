from typing import List, Optional

import numpy as np
from numpy.typing import NDArray

from outlines.text.generate.sequence import Sequence


class Continuation(Sequence):
    """Represents a completion generation model.

    `Completion` instances are unconstrained generation models that stop when an EOS token
    has been found or when the maximum number of tokens has been reached.

    >> import outlines.text as text
    >> sequence = text.sequence(model)("Say something")

    """

    def __init__(self, model, max_tokens: Optional[int]):
        super().__init__(model, max_tokens)

    def is_finished(self, token_ids: NDArray[np.int64]) -> NDArray[np.bool_]:
        """Determine whether the sequences reached maximum length of end with
        and EOS token.

        In practice, `Sequence`'s `__call__` methods only passed the `token_ids`
        of the sequences that haven't been marked as finished already, which is
        why we only need to look for the EOS token in the last element rather
        than in the whole sequence.

        Parameters
        ----------
        token_ids
            The input sequences.

        """
        is_finished = np.zeros((token_ids.shape[0],), dtype=np.bool_)
        is_finished[token_ids[:, -1] == self.model.tokenizer.eos_token_id] = True

        return is_finished

    def postprocess_completions(self, completions: List[str]) -> List[str]:
        """Remove the EOS token from the completion."""
        return [
            completion.replace(self.model.tokenizer.eos_token, "")
            for completion in completions
        ]


def continuation(model, max_tokens: Optional[int] = None):
    return Continuation(model, max_tokens)
