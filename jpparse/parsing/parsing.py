"""Main script for parsing functionality, including fugashi to parse text."""

from fugashi import Tagger

from ..types import ParsedScript, RawScript, ScriptLine, ScriptMetadata, UnidicFeatures29, Vocab


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
    

    def parse_word(self, fugashi_word) -> Vocab | None:
        """Parse a fugashi word into a Vocab object.
        
        Args:
            fugashi_word: The fugashi word to parse.
        
        Returns:
            Vocab: The parsed Vocab object.
        """
        word_features = UnidicFeatures29.from_fugashi(fugashi_word.feature, analysis_dict=self.analysis_dict)

        if word_features is None:
            return None

        return None


    def parse_line(self, line: str) -> ScriptLine:
        """Parse a single line into a ScriptLine object.
        
        Args:
            line (str): The line to parse.
        
        Returns:
            ScriptLine: The parsed line.
        """
        words = self.tagger(line)

        vocab_breakdown = [self.parse_word(fugashi_word) for fugashi_word in words]
        vocab_breakdown = [vocab for vocab in vocab_breakdown if vocab is not None]

        return ScriptLine(text=line, vocab_breakdown=vocab_breakdown)
    
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
        