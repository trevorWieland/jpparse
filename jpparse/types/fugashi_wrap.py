"""Type wrappers for the fugashi library."""

from enum import Enum
from typing import Any, Optional

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, ValidationError, core_schema


class UnidicField(str):
    """Parent class for Unidic fields."""

    @classmethod
    def from_fugashi(cls, field: str | None, analysis_mode: bool = False) -> tuple[Optional["UnidicField"], Optional[str]]:
        """Convert a fugashi field to a UnidicField object.

        Args:
            field (str): The fugashi field to convert.
            analysis_mode (bool, optional): Whether to return the field as a string if it cannot be converted. Defaults to False.

        Returns:
            tuple[Optional["UnidicField"], Optional[str]]: The converted UnidicField object and the field if it could not be converted and analysis_mode was set.
        """
        try:
            if field == "*":
                return None, None
            if field is None:
                return None, None
            return cls(field), None
        except ValueError as e:
            if analysis_mode:
                return None, field
            else:
                raise ValueError(f"Invalid value for {cls.__name__}: {field}") from e

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable.

        Returns:
            bool: Whether the field is one-hot encodeable.
        """
        raise NotImplementedError

    @classmethod
    def get_onehot_order(cls) -> list[str] | None:
        """Get the order of the one-hot encoding for the field, or None if the field is not one-hot encodeable.

        Returns:
            list[str] | None: The order of the one-hot encoding for the field, or None if the field is not one-hot encodeable.
        """
        raise NotImplementedError

    def to_onehot(self) -> NDArray[np.int8]:
        """Convert the field to a one-hot encoded numpy array.

        Returns:
            NDArray[np.int8]: The one-hot encoded numpy array

        Raises:
            RuntimeError: If the field is not one-hot encodeable.
        """
        if self.is_onehot_encodeable():
            onehot = np.zeros(len(self.get_onehot_order()), dtype=np.int8)
            onehot[self.get_onehot_order().index(self.value)] = 1
            return onehot
        else:
            raise RuntimeError(f"{self.__class__.__name__} is not one-hot encodeable.")



class UnidicPos1(UnidicField, Enum):
    """Enum for the first part of speech in Unidic."""

    noun = "名詞"
    supplementary = "補助記号"
    particle = "助詞"
    verb = "動詞"
    auxiliary = "助動詞"
    suffix = "接尾辞"
    prefix = "接頭辞"
    interjection = "感動詞"
    adverb = "副詞"
    i_adjective = "形容詞"
    na_adjective = "形状詞"
    blank_space = "空白"
    symbol = "記号"
    conjunction = "接続詞"
    pronoun = "代名詞"
    prenoun_adj = "連体詞"
    other = "その他"

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable.

        Returns:
            bool: Whether the field is one-hot encodeable.
        """
        return True

    @classmethod
    def get_onehot_order(cls) -> list[str]:
        """Get the order of the one-hot encoding for the field.

        Returns:
            list[str]: The order of the one-hot encoding for the field.
        """
        return sorted(list(set(cls.__members__.values())))


class UnidicPos2(UnidicField, Enum):
    """Enum for the second part of speech in Unidic."""

    common_noun = "普通名詞"
    proper_noun = "固有名詞"
    character = "文字"
    case_particle = "格助詞"
    adverbial_particle = "副助詞"
    auxiliary_verb_stem = "助動詞語幹"
    open_bracket = "括弧開"
    close_bracket = "括弧閉"
    numeral = "数詞"
    filler = "フィラー"
    binding_particle = "係助詞"
    ending_particle = "終助詞"
    irregular_verb = "非自立可能"
    nominal = "名詞的"
    period = "句点"
    tari = "タリ"
    comma = "読点"
    conjunctive_particle = "接続助詞"
    ordinary = "一般"
    verbal = "動詞的"
    i_adjectival = "形容詞的"
    na_adjectival = "形状詞的"
    whole_phrase_particle = "準体助詞"
    error = "ＡＡ"  # No idea what caused this, but it appeared once
    other = "その他"

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable."""
        return True

    @classmethod
    def get_onehot_order(cls) -> list[str]:
        """Get the order of the one-hot encoding for the field."""
        return sorted(list(set(cls.__members__.values())))


class UnidicPos3(UnidicField, Enum):
    """Enum for the third part of speech in Unidic."""

    ordinary = "一般"
    place_name = "地名"
    person_name = "人名"
    counter_suffix = "助数詞"
    potential_counter_suffix = "助数詞可能"
    potential_na_adjective = "形状詞可能"
    potential_adverb = "副詞可能"
    sa_conversion = "サ変可能"
    sa_na_conversion = "サ変形状詞可能"
    emoticon = "顔文字"
    other = "その他"

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable."""
        return True

    @classmethod
    def get_onehot_order(cls) -> list[str]:
        """Get the order of the one-hot encoding for the field."""
        return [
            cls.ordinary,
            cls.place_name,
            cls.person_name,
            cls.counter_suffix,
            cls.potential_counter_suffix,
            cls.potential_na_adjective,
            cls.potential_adverb,
            cls.sa_conversion,
            cls.sa_na_conversion,
            cls.emoticon,
            cls.other,
        ]


class UnidicPos4(UnidicField, Enum):
    """Enum for the fourth part of speech in Unidic."""

    country_name = "国"
    first_name = "名"
    family_name = "姓"
    ordinary = "一般"
    other = "その他"

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable."""
        return True

    @classmethod
    def get_onehot_order(cls) -> list[str]:
        """Get the order of the one-hot encoding for the field."""
        return [
            cls.country_name,
            cls.first_name,
            cls.family_name,
            cls.ordinary,
            cls.other,
        ]


class UnidicCType(UnidicField, Enum):
    """Enum for the conjugation type in Unidic."""

    irregular_ka = "カ行変格"
    irregular_sa = "サ行変格"

    ichidan_higher_a = "上一段-ア行"
    ichidan_higher_ka = "上一段-カ行"
    ichidan_higher_ga = "上一段-ガ行"
    ichidan_higher_za = "上一段-ザ行"
    ichidan_higher_ta = "上一段-タ行"
    ichidan_higher_na = "上一段-ナ行"
    ichidan_higher_ha = "上一段-ハ行"
    ichidan_higher_ba = "上一段-バ行"
    ichidan_higher_ma = "上一段-マ行"
    ichidan_higher_ra = "上一段-ラ行"

    ichidan_lower_a = "下一段-ア行"
    ichidan_lower_ka = "下一段-カ行"
    ichidan_lower_ga = "下一段-ガ行"
    ichidan_lower_sa = "下一段-サ行"
    ichidan_lower_za = "下一段-ザ行"
    ichidan_lower_ta = "下一段-タ行"
    ichidan_lower_da = "下一段-ダ行"
    ichidan_lower_na = "下一段-ナ行"
    ichidan_lower_ha = "下一段-ハ行"
    ichidan_lower_ba = "下一段-バ行"
    ichidan_lower_ma = "下一段-マ行"
    ichidan_lower_ra = "下一段-ラ行"

    godan_ka = "五段-カ行"
    godan_ga = "五段-ガ行"
    godan_sa = "五段-サ行"
    godan_ta = "五段-タ行"
    godan_na = "五段-ナ行"
    godan_ba = "五段-バ行"
    godan_ma = "五段-マ行"
    godan_ra = "五段-ラ行"
    godan_wa = "五段-ワア行"

    auxiliary_ja = "助動詞-ジャ"
    auxiliary_ta = "助動詞-タ"
    auxiliary_tai = "助動詞-タイ"
    auxiliary_da = "助動詞-ダ"
    auxiliary_dosu = "助動詞-ドス"
    auxiliary_desu = "助動詞-デス"
    auxiliary_nai = "助動詞-ナイ"
    auxiliary_nanda = "助動詞-ナンダ"
    auxiliary_nu = "助動詞-ヌ"
    auxiliary_mai = "助動詞-マイ"
    auxiliary_masu = "助動詞-マス"
    auxiliary_ya = "助動詞-ヤ"
    auxiliary_rashii = "助動詞-ラシイ"
    auxiliary_rare = "助動詞-レル"
    auxiliary_hin = "助動詞-ヒン"
    auxiliary_hen = "助動詞-ヘン"
    auxiliary_yan = "助動詞-ヤン"
    auxiliary_nsu = "助動詞-ンス"

    i_adjective = "形容詞"

    text_irregular_sa = "文語サ行変格"
    text_irregular_ra = "文語ラ行変格"

    text_nidan_lower_ra = "文語下二段-ラ行"
    text_nidan_lower_a = "文語下二段-ア行"
    text_nidan_lower_sa = "文語下二段-サ行"
    text_nidan_lower_da = "文語下二段-ダ行"

    text_auxiliary_ki = "文語助動詞-キ"
    text_auxiliary_gotoshi = "文語助動詞-ゴトシ"
    text_auxiliary_zu = "文語助動詞-ズ"
    text_auxiliary_tari_complete = "文語助動詞-タリ-完了"
    text_auxiliary_tari_assertion = "文語助動詞-タリ-断定"
    text_auxiliary_nari_assertion = "文語助動詞-ナリ-断定"
    text_auxiliary_beshi = "文語助動詞-ベシ"
    text_auxiliary_mu = "文語助動詞-ム"
    text_auxiliary_ri = "文語助動詞-リ"
    text_auxiliary_keri = "文語助動詞-ケリ"
    text_auxiliary_maji = "文語助動詞-マジ"

    text_yondan_ha = "文語四段-ハ行"
    text_yondan_sa = "文語四段-サ行"
    text_yondan_ra = "文語四段-ラ行"
    text_yondan_ka = "文語四段-カ行"
    text_yondan_ta = "文語四段-タ行"
    text_yondan_ba = "文語四段-バ行"
    text_yondan_ma = "文語四段-マ行"

    text_i_adjective_ku = "文語形容詞-ク"
    text_i_adjective_shiku = "文語形容詞-シク"

    unchanging_type = "無変化型"
    special_type = "特殊型"

    other = "その他"

    def is_godan(self) -> bool:
        """Check if the conjugation type is a godan verb."""
        return self in [
            self.godan_ka,
            self.godan_ga,
            self.godan_sa,
            self.godan_ta,
            self.godan_na,
            self.godan_ba,
            self.godan_ma,
            self.godan_ra,
            self.godan_wa,
        ]

    def is_ichidan(self) -> bool:
        """Check if the conjugation type is an ichidan verb."""
        return self in [
            self.ichidan_higher_a,
            self.ichidan_higher_ka,
            self.ichidan_higher_ga,
            self.ichidan_higher_za,
            self.ichidan_higher_ta,
            self.ichidan_higher_na,
            self.ichidan_higher_ha,
            self.ichidan_higher_ba,
            self.ichidan_higher_ma,
            self.ichidan_higher_ra,
            self.ichidan_lower_a,
            self.ichidan_lower_ka,
            self.ichidan_lower_ga,
            self.ichidan_lower_sa,
            self.ichidan_lower_za,
            self.ichidan_lower_ta,
            self.ichidan_lower_da,
            self.ichidan_lower_na,
            self.ichidan_lower_ha,
            self.ichidan_lower_ba,
            self.ichidan_lower_ma,
            self.ichidan_lower_ra,
        ]

    def is_irregular(self) -> bool:
        """Check if the conjugation type is an irregular verb."""
        return self in [
            self.irregular_ka,
            self.irregular_sa,
            self.unchanging_type,
            self.special_type,
            self.text_irregular_sa,
            self.text_irregular_ra,
        ]

    def is_auxiliary(self) -> bool:
        """Check if the conjugation type is an auxiliary verb."""
        return self in [
            self.auxiliary_ja,
            self.auxiliary_ta,
            self.auxiliary_tai,
            self.auxiliary_da,
            self.auxiliary_dosu,
            self.auxiliary_desu,
            self.auxiliary_nai,
            self.auxiliary_nanda,
            self.auxiliary_nu,
            self.auxiliary_mai,
            self.auxiliary_masu,
            self.auxiliary_ya,
            self.auxiliary_rashii,
            self.auxiliary_rare,
            self.auxiliary_hin,
            self.auxiliary_hen,
            self.auxiliary_yan,
            self.auxiliary_nsu,
            self.text_auxiliary_ki,
            self.text_auxiliary_gotoshi,
            self.text_auxiliary_zu,
            self.text_auxiliary_tari_complete,
            self.text_auxiliary_tari_assertion,
            self.text_auxiliary_nari_assertion,
            self.text_auxiliary_beshi,
            self.text_auxiliary_mu,
            self.text_auxiliary_ri,
            self.text_auxiliary_keri,
            self.text_auxiliary_maji,
        ]

    def is_nidan(self) -> bool:
        """Check if the conjugation type is a nidan verb."""
        return self in [
            self.text_nidan_lower_ra,
            self.text_nidan_lower_a,
            self.text_nidan_lower_sa,
            self.text_nidan_lower_da,
        ]

    def is_yondan(self) -> bool:
        """Check if the conjugation type is a yondan verb."""
        return self in [
            self.text_yondan_ha,
            self.text_yondan_sa,
            self.text_yondan_ra,
            self.text_yondan_ka,
            self.text_yondan_ta,
            self.text_yondan_ba,
            self.text_yondan_ma,
        ]

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable."""
        return True

    @classmethod
    def get_onehot_order(cls) -> list[str]:
        """Get the order of the one-hot encoding for the field."""
        return sorted(list(set(cls.__members__.values())))


class UnidicCForm(UnidicField, Enum):
    """Enum for the conjugation form in Unidic."""

    conditional_general = "仮定形-一般"
    conditional_fusion = "仮定形-融合"

    realis_general = "已然形-一般"
    realis_auxiliary = "已然形-補助"

    imperative = "命令形"

    volitional_nominal = "意志推量形"

    imperfective_sa = "未然形-サ"
    imperfective_se = "未然形-セ"
    imperfective_general = "未然形-一般"
    imperfective_nasal_n = "未然形-撥音便"
    imperfective_auxiliary = "未然形-補助"

    conclusive_general = "終止形-一般"
    conclusive_nasal_t = "終止形-促音便"
    conclusive_nasal_n = "終止形-撥音便"
    conclusive_auxiliary = "終止形-補助"
    conclusive_fusion = "終止形-融合"

    stem_sa = "語幹-サ"
    stem_general = "語幹-一般"

    attributive_general = "連体形-一般"
    attributive_nasal_n = "連体形-撥音便"
    attributive_omission = "連体形-省略"
    attributive_auxiliary = "連体形-補助"
    attrivutive_i = "連体形-イ音便"

    continuative_i = "連用形-イ音便"
    continuative_u = "連用形-ウ音便"
    continuative_ni = "連用形-ニ"
    continuative_to = "連用形-ト"
    continuative_general = "連用形-一般"
    continuative_nasal_n = "連用形-撥音便"
    continuative_nasal_t = "連用形-促音便"
    continuative_omission = "連用形-省略"
    continuative_auxiliary = "連用形-補助"
    continuative_fusion = "連用形-融合"

    ku_form = "ク語法"

    other = "その他"

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable."""
        return True

    @classmethod
    def get_onehot_order(cls) -> list[str]:
        """Get the order of the one-hot encoding for the field."""
        return sorted(list(set(cls.__members__.values())))


class UnidicGoshu(UnidicField, Enum):
    """Enum for the goshu field in Unidic."""

    japan = "和"  # Japanese origin word
    solid = "固"  # Solid compound word
    china = "漢"  # Chinese origin word
    foreign = "外"  # Foreign origin word
    mixed = "混"  # Mixed origin word
    symbol = "記号"  # Symbol
    unknown = "不明"  # Unknown origin word
    other = "その他"

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable."""
        return True

    @classmethod
    def get_onehot_order(cls) -> list[str]:
        """Get the order of the one-hot encoding for the field."""
        return sorted(list(set(cls.__members__.values())))


class UnidicType(UnidicField, Enum):
    """Enum for the type field in Unidic."""

    human_counter = "体"  # Not sure what this means
    binding_particle = "係助"  # Binding particle
    support = "補助"  # Support
    country = "国"  # Country
    case_making_particle = "格助"  # Case making particle
    auxiliary = "助動"  # Auxiliary
    use = "用"  # 'Use' not sure what this means
    proper_name = "固有名"  # Proper name
    person_name = "人名"  # Person name
    place_name = "地名"  # Place name
    symbol = "記号"  # Symbol
    number = "数"  # Number
    supporter = "準助"  # Supporter
    conjunctive = "接助"  # Conjunctive
    suffix1 = "接尾用"  # Suffix 1 - Need to clarify
    suffix2 = "接尾相"  # Suffix 2 - Need to clarify
    suffix3 = "接尾体"  # Suffix 3 - Need to clarify
    assisting_particle = "副助"  # Assisting particle
    counter = "助数"  # Counter
    first_name = "名"  # First name
    family_name = "姓"  # Family name
    prefix = "接頭"  # Prefix
    ending_particle = "終助"  # Ending particle
    aspect = "相"  # Aspect
    other = "他"

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable."""
        return True

    @classmethod
    def get_onehot_order(cls) -> list[str]:
        """Get the order of the one-hot encoding for the field."""
        return sorted(list(set(cls.__members__.values())))


class UnidicGeneralString(UnidicField):
    """General string field for Unidic."""

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        """Validate the field as a general string."""
        return core_schema.no_info_after_validator_function(cls, handler(str))

    @classmethod
    def is_onehot_encodeable(cls) -> bool:
        """Check if the field is one-hot encodeable."""
        return False

    @classmethod
    def get_onehot_order(cls) -> None:
        """Get the order of the one-hot encoding for the field."""
        return None


class UnidicFeatures29(BaseModel):
    """Conversion of named tuple to Pydantic model.

    Attributes:
        pos1: The most general way of representing the part of speech.
        pos2: The second most general way of representing the part of speech.
        pos3: The third most general way of representing the part of speech.
        pos4: The most specific way of representing the part of speech.
        cType: The type of conjugation.
        cForm: The form of conjugation.
        lForm: The lemma form of the word.
        lemma: The lemma of the word.
        orth: The word as it appears in the text.
        pron: The pronunciation of the word.
        orthBase: The uninflected form of the word in context.
        pronBase: The pronunciation of orthBase.
        goshu: The basic etymology of the word.
        iType: The type of initial transformation.
        iForm: The initial form of the word in context.
        fType: The type of final transformation.
        fForm: The final form of the word in context.
        iConType: The type of initial change fusion.
        fConType: The type of final change fusion.
        type: The type of the lemma.
        kana: The katakana representation of the word.
        kanaBase: The katakana representation of the lemma.
        form: The form of the word.
        formBase: The uninflected form of the word.
        aType: The accent type of the word.
        aConType: The accent change type of the word.
        aModType: The accent modification type of the word.
        lid: The lexical ID of the word. Mostly unique, except for half/full width versions of the same lemma.
        lemma_id: The lemma ID of the word. Unique per lemma, but not per word.

    Todo:
        Add stricter type checking for all remaining str fields.
    """

    pos1: UnidicPos1 | None = Field(
        ..., title="Part of Speech 1", description="The most general way of representing the part of speech."
    )
    pos2: UnidicPos2 | None = Field(
        ..., title="Part of Speech 2", description="The second most general way of representing the part of speech."
    )
    pos3: UnidicPos3 | None = Field(
        ..., title="Part of Speech 3", description="The third most general way of representing the part of speech."
    )
    pos4: UnidicPos4 | None = Field(
        ..., title="Part of Speech 4", description="The most specific way of representing the part of speech."
    )
    cType: UnidicCType | None = Field(..., title="Conjugation Type", description="The type of conjugation.")
    cForm: UnidicCForm | None = Field(..., title="Conjugation Form", description="The form of conjugation.")
    lForm: str = Field(..., title="Lemma Form", description="The lemma form of the word.")
    lemma: str = Field(..., title="Lemma", description="The lemma of the word.")
    orth: str = Field(..., title="Orthography", description="The word as it appears in the text.")
    pron: str = Field(..., title="Pronunciation", description="The pronunciation of the word.")
    orthBase: str = Field(..., title="Base Orthography", description="The uninflected form of the word in context.")
    pronBase: str = Field(..., title="Base Pronunciation", description="The pronunciation of orthBase.")
    goshu: UnidicGoshu | None = Field(..., title="Goshu", description="The basic etymology of the word.")
    iType: UnidicGeneralString | None = Field(
        ..., title="Initial Transformation", description="The type of initial transformation."
    )
    iForm: UnidicGeneralString | None = Field(
        ..., title="Initial Form", description="The initial form of the word in context."
    )
    fType: UnidicGeneralString | None = Field(
        ..., title="Final Transformation", description="The type of final transformation."
    )
    fForm: UnidicGeneralString | None = Field(
        ..., title="Final Form", description="The final form of the word in context."
    )
    iConType: UnidicGeneralString | None = Field(
        ..., title="Initial change fusion type", description="The type of initial change fusion."
    )
    fConType: UnidicGeneralString | None = Field(
        ..., title="Final change fusion type", description="The type of final change fusion."
    )
    type: UnidicType | None = Field(..., title="Type", description="The type of the lemma.")
    kana: str = Field(..., title="Kana", description="The katakana representation of the word.")
    kanaBase: str = Field(..., title="Base Kana", description="The katakana representation of the lemma.")
    form: str = Field(..., title="Form", description="The form of the word.")
    formBase: str = Field(..., title="Base Form", description="The uninflected form of the word.")
    aType: str = Field(..., title="Accent Type", description="The accent type of the word.")
    aConType: str = Field(..., title="Accent change type", description="The accent change type of the word.")
    aModType: UnidicGeneralString | None = Field(
        ..., title="Accent modification type", description="The accent modification type of the word."
    )
    lid: int = Field(
        ...,
        title="Lexical ID",
        description="The lexical ID of the word. Mostly unique, except for half/full width versions of the same lemma.",
    )
    lemma_id: int = Field(
        ..., title="Lemma ID", description="The lemma ID of the word. Unique per lemma, but not per word."
    )

    @classmethod
    def from_fugashi(cls, feature, analysis_dict: dict[str, set[str]] | None = None) -> Optional["UnidicFeatures29"]:
        """Convert a fugashi word object to a UnidicFeatures29 object.

        Args:
            feature: The fugashi word object to convert.
            analysis_dict: A dictionary of analysis fields to store unknown fields in. Defaults to None.

        Returns:
            UnidicFeatures29: The converted UnidicFeatures29 object.
        """
        if analysis_dict is None:
            return cls(
                pos1=UnidicPos1.from_fugashi(feature.pos1)[0],
                pos2=UnidicPos2.from_fugashi(feature.pos2)[0],
                pos3=UnidicPos3.from_fugashi(feature.pos3)[0],
                pos4=UnidicPos4.from_fugashi(feature.pos4)[0],
                cType=UnidicCType.from_fugashi(feature.cType)[0],
                cForm=UnidicCForm.from_fugashi(feature.cForm)[0],
                lForm=feature.lForm if feature.lForm is not None else "",
                lemma=feature.lemma if feature.lemma is not None else "",
                orth=feature.orth if feature.orth is not None else "",
                pron=feature.pron if feature.pron is not None else "",
                orthBase=feature.orthBase if feature.orthBase is not None else "",
                pronBase=feature.pronBase if feature.pronBase is not None else "",
                goshu=UnidicGoshu.from_fugashi(feature.goshu)[0],
                iType=UnidicGeneralString.from_fugashi(feature.iType)[0],
                iForm=UnidicGeneralString.from_fugashi(feature.iForm)[0],
                fType=UnidicGeneralString.from_fugashi(feature.fType)[0],
                fForm=UnidicGeneralString.from_fugashi(feature.fForm)[0],
                iConType=UnidicGeneralString.from_fugashi(feature.iConType)[0],
                fConType=UnidicGeneralString.from_fugashi(feature.fConType)[0],
                type=UnidicType.from_fugashi(feature.type)[0],
                kana=feature.kana if feature.kana is not None else "",
                kanaBase=feature.kanaBase if feature.kanaBase is not None else "",
                form=feature.form if feature.form is not None else "",
                formBase=feature.formBase if feature.formBase is not None else "",
                aType=feature.aType if feature.aType is not None else "",
                aConType=feature.aConType if feature.aConType is not None else "",
                aModType=UnidicGeneralString.from_fugashi(feature.aModType)[0],
                lid=feature.lid if feature.lid is not None else 0,
                lemma_id=feature.lemma_id if feature.lemma_id is not None else 0,
            )
        else:
            cls_dict = {}
            cls_dict["pos1"], raw_field = UnidicPos1.from_fugashi(feature.pos1, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["pos1"] = analysis_dict.get("pos1", set()) | {raw_field}
            cls_dict["pos2"], raw_field = UnidicPos2.from_fugashi(feature.pos2, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["pos2"] = analysis_dict.get("pos2", set()) | {raw_field}
            cls_dict["pos3"], raw_field = UnidicPos3.from_fugashi(feature.pos3, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["pos3"] = analysis_dict.get("pos3", set()) | {raw_field}
            cls_dict["pos4"], raw_field = UnidicPos4.from_fugashi(feature.pos4, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["pos4"] = analysis_dict.get("pos4", set()) | {raw_field}
            cls_dict["cType"], raw_field = UnidicCType.from_fugashi(feature.cType, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["cType"] = analysis_dict.get("cType", set()) | {raw_field}
            cls_dict["cForm"], raw_field = UnidicCForm.from_fugashi(feature.cForm, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["cForm"] = analysis_dict.get("cForm", set()) | {raw_field}
            cls_dict["lForm"] = feature.lForm
            cls_dict["lemma"] = feature.lemma
            cls_dict["orth"] = feature.orth
            cls_dict["pron"] = feature.pron
            cls_dict["orthBase"] = feature.orthBase
            cls_dict["pronBase"] = feature.pronBase
            cls_dict["goshu"], raw_field = UnidicGoshu.from_fugashi(feature.goshu, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["goshu"] = analysis_dict.get("goshu", set()) | {raw_field}
            cls_dict["iType"], raw_field = UnidicGeneralString.from_fugashi(feature.iType, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["iType"] = analysis_dict.get("iType", set()) | {raw_field}
            cls_dict["iForm"], raw_field = UnidicGeneralString.from_fugashi(feature.iForm, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["iForm"] = analysis_dict.get("iForm", set()) | {raw_field}
            cls_dict["fType"], raw_field = UnidicGeneralString.from_fugashi(feature.fType, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["fType"] = analysis_dict.get("fType", set()) | {raw_field}
            cls_dict["fForm"], raw_field = UnidicGeneralString.from_fugashi(feature.fForm, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["fForm"] = analysis_dict.get("fForm", set()) | {raw_field}
            cls_dict["iConType"], raw_field = UnidicGeneralString.from_fugashi(feature.iConType, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["iConType"] = analysis_dict.get("iConType", set()) | {raw_field}
            cls_dict["fConType"], raw_field = UnidicGeneralString.from_fugashi(feature.fConType, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["fConType"] = analysis_dict.get("fConType", set()) | {raw_field}
            cls_dict["type"], raw_field = UnidicType.from_fugashi(feature.type, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["type"] = analysis_dict.get("type", set()) | {raw_field}
            cls_dict["kana"] = feature.kana
            cls_dict["kanaBase"] = feature.kanaBase
            cls_dict["form"] = feature.form
            cls_dict["formBase"] = feature.formBase
            cls_dict["aType"] = feature.aType
            cls_dict["aConType"] = feature.aConType
            cls_dict["aModType"], raw_field = UnidicGeneralString.from_fugashi(feature.aModType, analysis_mode=True)
            if raw_field is not None:
                analysis_dict["aModType"] = analysis_dict.get("aModType", set()) | {raw_field}
            cls_dict["lid"] = feature.lid
            cls_dict["lemma_id"] = feature.lemma_id

            try:
                return cls(**cls_dict)
            except ValidationError:
                return None

    def to_onehot(self) -> NDArray[np.int8]:
        """Convert the object to a one-hot encoded matrix.

        Pads the one-hot encoding with zeros to ensure that all fields are the same length.
        The shape of this matrix is (n_fields, max_field_length).
        If a given field is None, all values in that row will be set to 0.

        Returns:
            NDArray[np.int8]: The one-hot encoded array.
        """
        onehot = []
        max_length = 0

        if self.pos1 is not None:
            onehot.append(self.pos1.to_onehot())
        else:
            onehot.append(np.zeros(len(UnidicPos1.get_onehot_order()), dtype=np.int8))
        max_length = max(max_length, len(UnidicPos1.get_onehot_order()))

        if self.pos2 is not None:
            onehot.append(self.pos2.to_onehot())
        else:
            onehot.append(np.zeros(len(UnidicPos2.get_onehot_order()), dtype=np.int8))
        max_length = max(max_length, len(UnidicPos2.get_onehot_order()))

        if self.pos3 is not None:
            onehot.append(self.pos3.to_onehot())
        else:
            onehot.append(np.zeros(len(UnidicPos3.get_onehot_order()), dtype=np.int8))
        max_length = max(max_length, len(UnidicPos3.get_onehot_order()))

        if self.pos4 is not None:
            onehot.append(self.pos4.to_onehot())
        else:
            onehot.append(np.zeros(len(UnidicPos4.get_onehot_order()), dtype=np.int8))
        max_length = max(max_length, len(UnidicPos4.get_onehot_order()))

        if self.cType is not None:
            onehot.append(self.cType.to_onehot())
        else:
            onehot.append(np.zeros(len(UnidicCType.get_onehot_order()), dtype=np.int8))
        max_length = max(max_length, len(UnidicCType.get_onehot_order()))

        if self.cForm is not None:
            onehot.append(self.cForm.to_onehot())
        else:
            onehot.append(np.zeros(len(UnidicCForm.get_onehot_order()), dtype=np.int8))
        max_length = max(max_length, len(UnidicCForm.get_onehot_order()))

        if self.goshu is not None:
            onehot.append(self.goshu.to_onehot())
        else:
            onehot.append(np.zeros(len(UnidicGoshu.get_onehot_order()), dtype=np.int8))
        max_length = max(max_length, len(UnidicGoshu.get_onehot_order()))

        if self.type is not None:
            onehot.append(self.type.to_onehot())
        else:
            onehot.append(np.zeros(len(UnidicType.get_onehot_order()), dtype=np.int8))
        max_length = max(max_length, len(UnidicType.get_onehot_order()))

        # Pad all one-hot encodings to the same length
        for i in range(len(onehot)):
            onehot[i] = np.pad(onehot[i], (0, max_length - len(onehot[i])), "constant")

        return np.vstack(onehot)
