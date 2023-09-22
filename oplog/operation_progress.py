from typing import Optional, Final, Tuple, Iterable

from tqdm.auto import tqdm


class OperationProgress:
    PROGRESS_INDENT: Final[str] = '--'

    def __init__(self,
                 iterations: Optional[Tuple[int, float]],
                 pbar_descriptor: Optional[str] = None,
                 ancestors_progress: Optional[Iterable['OperationProgress']] = None,
                 ):
        """
        An extension that makes the operation progress-able, meaning it can declare progression
         using the `.progress()` method, and also display a progress bar.
         Note that the progress bar may not be displayed correctly in some IDEs
         (but will work in the terminal, notebooks, etc.).
        """
        self.iterations = iterations
        self.completion_ratio: Optional[float] = None
        self._pbar: Optional[tqdm] = None

        if pbar_descriptor:
            num_ancestors_pbar = len([p for p in ancestors_progress if p._pbar is not None])
            indent = num_ancestors_pbar * self.PROGRESS_INDENT + num_ancestors_pbar * ' '
            indent_pbar_desc = f'{indent}{pbar_descriptor}'
            self._pbar: Optional[tqdm] = tqdm(
                total=iterations,
                desc=indent_pbar_desc,
                # only keep progress bar of root-level operations
                leave=num_ancestors_pbar == 0
            )

    def progress(self, n: Optional[Tuple[int, float]] = 1):
        if self._pbar is not None:
            self._pbar.update(n)
        else:
            # todo update completion ratio
            pass

    def exit(self, is_successful: bool):
        if self._pbar is not None:
            if not is_successful:
                self._pbar.update(self._pbar.total - self._pbar.n)
            self._pbar.close()
        else:
            # todo update completion ratio
            pass
