"""Typing information for kanji, vocab, and grammar."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class VocabType(str, Enum):
    """Enum for storing the type of a vocab word."""

    noun = "noun"
    godan_verb = "godan_verb"
    ichidan_verb = "ichidan_verb"
    irregular_verb = "irregular_verb"
    i_adjective = "i_adjective"
    na_adjective = "na_adjective"
    adverb = "adverb"
    particle = "particle"
    pronoun = "pronoun"
    other = "other"


class VerbForm(str, Enum):
    """Enum for storing verb tenses/forms/conjugations."""

    prohibitive = "prohibitive"
    plain_negative = "plain_negative"
    passive = "passive"
    causative = "causative"
    command = "command"
    conditional = "conditional"
    possibility = "possibility"
    volitional = "volitional"
    masu = "masu"
    masen = "masen"
    polite_volitional = "polite_volitional"
    hierarchical_command = "hierarchical_command"
    te = "te"
    ta = "ta"
    tara = "tara"
    tai = "tai"
    naide = "naide"


class KanjiData(BaseModel):
    """Information about a specific kanji character in general."""

    character: str = Field(..., title="The character itself")
    freq_rank: int | None = Field(None, title="The frequency rank of this character")
    is_jinmeiyo: bool = Field(False, title="Whether this character is a Jinmeiyo Kanji")
    is_jouyou: bool = Field(False, title="Whether this character is a Jouyou Kanji")
    is_kyouiku: bool = Field(False, title="Whether this character is a Kyouiku Kanji")


class Kanji(BaseModel):
    """A single occurrence of a kanji character in a text."""

    character: str = Field(..., title="The character itself")
    data: KanjiData = Field(..., title="General data about this Kanji character")


class VocabData(BaseModel):
    """Information about a specific vocab word in general."""

    kana: str = Field(..., title="The kana of the word")
    common_spellings: list[str] = Field(..., title="Common spellings of the word, with/without kanji")
    freq_rank: int | None = Field(None, title="The frequency rank of this word")
    lemma_data: Optional["VocabData"] = Field(
        None, title="The data for the lemma of this word, if it is not the lemma itself", exclude=True
    )


class Vocab(BaseModel):
    """A single occurrence of a vocab word in a text."""

    word: str = Field(..., title="The word itself")
    reading: str = Field(..., title="The reading of the word in katakana")
    data: VocabData | None = Field(..., title="General data about this vocab word")
    type: VocabType = Field(..., title="The type of this vocab word")
    verb_forms: list[VerbForm] | None = Field(None, title="The form(s) of this verb, if it is a verb")
    component_kanji: list[Kanji] = Field(..., title="The kanji characters that make up this word, if any")
    component_vocab: list["Vocab"] = Field(..., title="The vocab words that make up this word, if any")
