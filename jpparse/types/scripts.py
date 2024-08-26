"""Typing information for handling the scripts."""

from enum import Enum

from pydantic import BaseModel, Field

from .text import Vocab


class ScriptCategory(str, Enum):
    """The category of a script."""

    visual_novel = "visual_novel"
    light_novel = "light_novel"
    manga = "manga"
    anime = "anime"
    drama_cd = "drama_cd"
    game = "game"
    other = "other"


class ScriptMetadata(BaseModel):
    """The metadata for a script."""

    name: str = Field(
        ...,
        description="The name of the script as stored in the filename. Use clean_name or jp_name for display purposes.",
        examples=["leyline1"],
    )
    clean_name: str = Field(
        ..., description="The name of the script for display purposes, in English.", examples=["A Clockwork Ley-Line"]
    )
    jp_name: str = Field(
        ...,
        description="The name of the script for display purposes, in Japanese.",
        examples=["時計仕掛けのレイライン"],
    )
    category: ScriptCategory = Field(..., description="The category of the script.", examples=["visual_novel"])
    vndb_id: int | None = Field(
        None,
        description="The VNDB ID of the script, if available. This is the 'v' id of a visual novel, shared across all releases.",
        examples=[10016],
    )
    vndb_release_id: int | None = Field(
        None,
        description="The VNDB ID of the release of the script, if available. This is the 'r' id of a visual novel release. Can be None even if the vndb id is available, in the case that we aren't sure which release the script is for.",
        examples=[None, 20155],
    )


class ScriptIndex(BaseModel):
    """The script index metadata file."""

    version: str = Field(
        ...,
        description="The version of the script index. Should follow semantic versioning, where any breaking change is a major version, any new feature / script is a minor version, and any bug fix / typo fix / missing lines is a patch version.",
        examples=["1.0.0"],
    )
    scripts: list[ScriptMetadata] = Field(
        ...,
        description="The metadata for all scripts in the index.",
        examples=[
            {
                "name": "leyline1",
                "clean_name": "A Clockwork Ley-Line",
                "jp_name": "時計仕掛けのレイライン",
                "category": "visual_novel",
                "vndb_id": 10016,
                "vndb_release_id": None,
            }
        ]
    )


class RawScript(BaseModel):
    """A raw script."""

    metadata: ScriptMetadata = Field(
        ...,
        description="The metadata for the script.",
        examples=[
            {
                "name": "leyline1",
                "clean_name": "A Clockwork Ley-Line",
                "jp_name": "時計仕掛けのレイライン",
                "category": "visual_novel",
                "vndb_id": 10016,
                "vndb_release_id": None,
            }
        ],
    )
    script: str = Field(..., description="The raw script text.")


class ScriptLine(BaseModel):
    """A single line from a script, containing all parsed kanji, vocab, and grammar."""

    text: str = Field(..., description="The text of the line.")

    # TODO: Add kanji, vocab, and grammar fields / difficulty metrics
    vocab_breakdown: list[Vocab] = Field(..., description="The best-guess vocab breakdown of the line.")


class ParsedScript(BaseModel):
    """A parsed script."""

    metadata: ScriptMetadata = Field(
        ...,
        description="The metadata for the script.",
        examples=[
            {
                "name": "leyline1",
                "clean_name": "A Clockwork Ley-Line",
                "jp_name": "時計仕掛けのレイライン",
                "category": "visual_novel",
                "vndb_id": 10016,
                "vndb_release_id": None,
            }
        ],
    )
    lines: list[ScriptLine] = Field(..., description="The parsed lines of the script.")

    # TODO: Add cumulative kanji, vocab, and grammar fields / difficulty metrics
