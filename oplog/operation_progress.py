from typing import Optional, Final, Iterable, Union

from tqdm.auto import tqdm


class ProgressNotAvailableException(Exception):
    pass


class OperationProgress:
    PROGRESS_INDENT: Final[str] = '--'

    def __init__(self,
                 iterations: Optional[Union[int, float]] = None,
                 pbar_descriptor: Optional[str] = None,
                 ancestors_progress: Optional[Iterable['OperationProgress']] = None,
                 ):
        """
        An extension that makes the operation progress-able,
        meaning it can declare progression
        using the `.progress()` method, and also display a progress bar.
        Note that the progress bar may not be displayed correctly in some IDEs
        (but will work in the terminal, notebooks, etc.).
        """
        self.iterations = iterations
        self.completion_ratio: Optional[float] = 0.0

        ancestors_progress = ancestors_progress or []
        if pbar_descriptor:
            num_ancestors_pbar = len([
                p for p in ancestors_progress if p._pbar is not None
            ])
            indent = (
                    (num_ancestors_pbar * self.PROGRESS_INDENT) +
                    (num_ancestors_pbar * ' ')
            )
            indent_pbar_desc = f'{indent}{pbar_descriptor}'
            pbar: Optional[tqdm] = tqdm(
                total=iterations,
                desc=indent_pbar_desc,
                # only keep progress bar of root-level operations
                leave=num_ancestors_pbar == 0
            )
        else:
            pbar = None

        self._pbar: Optional[tqdm] = pbar

    def progress(self, n: Union[int, float] = 1):
        if self._pbar is not None:
            self._pbar.update(n)

        if self.iterations is not None and self.completion_ratio is not None:
            steps_completed_thus_far = self.completion_ratio * self.iterations
            self.completion_ratio = (steps_completed_thus_far + n) / self.iterations

        if self._pbar is None and self.iterations is None:
            raise ProgressNotAvailableException(
                "`progress` method only has effect if either "
                "total number of iterations is specified "
                "or a progress bar is displayed."
            )

    def exit(self, is_successful: bool):
        if self._pbar is not None:
            if is_successful and self.iterations is not None:
                # fill progress bar
                self._pbar.update(self._pbar.total - self._pbar.n)
            self._pbar.close()

        if is_successful:
            self.completion_ratio = 1.0
        elif self.iterations is None:
            # unknown progress
            self.completion_ratio = None
