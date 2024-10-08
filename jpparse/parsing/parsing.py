"""Main script for parsing functionality, including fugashi to parse text."""

import numpy as np
from fugashi import Tagger
from numpy.typing import NDArray

from ..types import ParsedScript, RawScript, ScriptLine, ScriptMetadata, UnidicFeatures29


class ScriptParser:
    """Class for parsing a text."""

    def __init__(self, script: RawScript, analysis_mode: bool = False):
        """Create a ScriptParser from a RawScript object.

        Args:
            script (RawScript): The raw script to parse.
            analysis_mode (bool): Whether to run in analysis mode. Defaults to False.
        """
        self.metadata = script.metadata
        self.raw_lines = script.script.split("\n")

        self.tagger = Tagger("-Owakati")
        self.parsed_script: ParsedScript | None = None

        self.analysis_dict: dict[str, set[str]] | None = None if not analysis_mode else {}

    def parse_word(self, fugashi_word) -> NDArray | None:
        """Attempt to parse a fugashi word into matrix form.

        Args:
            fugashi_word: The fugashi word to parse.

        Returns:
            NDArray: The parsed word in matrix form.
        """
        word_features = UnidicFeatures29.from_fugashi(fugashi_word.feature, analysis_dict=self.analysis_dict)

        if word_features is None:
            return None

        matrix = word_features.to_onehot()

        return matrix

    def parse_line(self, line: str) -> ScriptLine:
        """Parse a single line into a ScriptLine object.

        Args:
            line (str): The line to parse.

        Returns:
            ScriptLine: The parsed line.
        """
        words = self.tagger(line)

        grammar_slices = [self.parse_word(fugashi_word) for fugashi_word in words]
        grammar_slices = [grammar_slice for grammar_slice in grammar_slices if grammar_slice is not None]

        grammar_sum: NDArray = sum(grammar_slices)

        if len(grammar_slices) == 0:
            grammar_fingerprint = np.zeros((8, 81), dtype=np.float16)
        elif len(grammar_slices) == 1:
            grammar_fingerprint = grammar_slices[0]
        else:
            grammar_fingerprint = grammar_sum / len(grammar_slices)

        return ScriptLine(text=line, grammar_fingerprint=grammar_fingerprint.astype(np.float16))

    def parse(self) -> ParsedScript:
        """Parse the entire script into a list of ScriptLine objects.

        Returns:
            ParsedScript: The parsed script.
        """
        if self.parsed_script is not None:
            return self.parsed_script

        self.parsed_script = ParsedScript(
            metadata=self.metadata,
            lines=[self.parse_line(line) for line in self.raw_lines],
            fingerprint_version="0.1"
        )

        return self.parsed_script

    @classmethod
    def from_metadata(cls, metadata: ScriptMetadata, script_folder: str, analysis_mode: bool = False) -> "ScriptParser":
        """Create a ScriptParser from metadata and a script folder.

        Args:
            metadata (ScriptMetadata): The metadata for the script.
            script_folder (str): The folder containing the script.
            analysis_mode (bool): Whether to run in analysis mode. Defaults to False.

        Returns:
            ScriptParser: The created ScriptParser object.
        """
        with open(f"{script_folder}/{metadata.name}.txt", "r", encoding="utf-8") as f:
            script = f.read()

        raw_script = RawScript(metadata=metadata, script=script)

        return cls(raw_script, analysis_mode=analysis_mode)
