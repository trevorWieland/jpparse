"""Type wrappers for the fugashi library."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, ValidationError, core_schema


class UnidicField:
    """Parent class for Unidic fields."""

    @classmethod
    def from_fugashi(cls, field: str, analysis_mode: bool = False) -> tuple[Optional["UnidicField"], Optional[str]]:
        """Convert a fugashi field to a UnidicField object."""
        try:
            if field == "*":
                return None, None
            return cls(field), None
        except ValueError as e:
            if analysis_mode:
                return None, field
            else:
                raise ValueError(f"Invalid value for {cls.__name__}: {field}") from e


class UnidicPos1(UnidicField, str, Enum):
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

class UnidicPos2(UnidicField, str, Enum):
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
    other = "その他"

class UnidicPos3(UnidicField, str, Enum):
    """Enum for the third part of speech in Unidic."""

    ordinary = "一般"
    place_name = "地名"
    person_name = "人名"
    other = "その他"

class UnidicPos4(UnidicField, str, Enum):
    """Enum for the fourth part of speech in Unidic."""

    country_name = "国"
    first_name = "名"
    family_name = "姓"
    ordinary = "一般"
    other = "その他"

class UnidicCType(UnidicField, str, Enum):
    """Enum for the conjugation type in Unidic."""

    irregular_ka = "カ行変格"
    irregular_sa = "サ行変格"

    ichidan_higher_a = "上一段-ア行"
    ichidan_higher_ka = "上一段-カ行"
    ichidan_higher_ga = "上一段-ガ行"
    ichidan_higher_za = "上一段-ザ行"
    ichidan_higher_ta = "上一段-タ行"
    ichidan_higher_na = "上一段-ナ行"
    ichidan_higher_ba = "上一段-バ行"
    ichidan_higher_ma = "上一段-マ行"
    ichidan_higher_ra = "上一段-ラ行"

    ichidan_lower_a = "下一段-ア行"
    ichidan_lower_ka = "下一段-カ行"
    ichidan_lower_ga = "下一段-ガ行"
    ichidan_lower_sa = "下一段-サ行"
    ichidan_lower_ta = "下一段-タ行"
    ichidan_lower_da = "下一段-ダ行"
    ichidan_lower_na = "下一段-ナ行"
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
    auxiliary_desu = "助動詞-デス"
    auxiliary_nai = "助動詞-ナイ"
    auxiliary_nanda = "助動詞-ナンダ"
    auxiliary_nu = "助動詞-ヌ"
    auxiliary_mai = "助動詞-マイ"
    auxiliary_masu = "助動詞-マス"
    auxiliary_ya = "助動詞-ヤ"
    auxiliary_rashii = "助動詞-ラシイ"
    auxiliary_rare = "助動詞-レル"

    i_adjective = "形容詞"

    text_irregular_sa = "文語サ行変格"
    text_irregular_ra = "文語ラ行変格"

    text_ichidan_double_lower_ra = "文語下二段-ラ行"

    text_auxiliary_ki = "文語助動詞-キ"
    text_auxiliary_gotoshi = "文語助動詞-ゴトシ"
    text_auxiliary_zu = "文語助動詞-ズ"
    text_auxiliary_tari_complete = "文語助動詞-タリ-完了"
    text_auxiliary_tari_assertion = "文語助動詞-タリ-断定"
    text_auxiliary_nari_assertion = "文語助動詞-ナリ-断定"
    text_auxiliary_beshi = "文語助動詞-ベシ"
    text_auxiliary_mu = "文語助動詞-ム"
    text_auxiliary_ri = "文語助動詞-リ"

    text_yondan_ha = "文語四段-ハ行"

    text_i_adjective_ku = "文語形容詞-ク"
    text_i_adjective_shiku = "文語形容詞-シク"

    other = "その他"

class UnidicCForm(UnidicField, str, Enum):
    """Enum for the conjugation form in Unidic."""


    other = "その他"

class UnidicGoshu(UnidicField, str, Enum):
    """Enum for the goshu field in Unidic."""

    japan = "和" # Japanese origin word
    solid = "固" # Solid compound word
    china = "漢" # Chinese origin word
    foreign = "外" # Foreign origin word
    mixed = "混" # Mixed origin word
    symbol = "記号" # Symbol
    unknown = "不明" # Unknown origin word
    other = "その他"

class UnidicType(UnidicField, str, Enum):
    """Enum for the type field in Unidic."""

    human_counter = "体" # Not sure what this means
    binding_particle = "係助" # Binding particle
    support = "補助" # Support
    country = "国" # Country
    case_making_particle = "格助" # Case making particle
    auxiliary = "助動" # Auxiliary
    use = "用" # 'Use' not sure what this means
    proper_name = "固有名" # Proper name
    person_name = "人名" # Person name
    place_name = "地名" # Place name
    symbol = "記号" # Symbol
    number = "数" # Number
    supporter = "準助" # Supporter
    conjunctive = "接助" # Conjunctive
    suffix1 = "接尾用" # Suffix 1 - Need to clarify
    suffix2 = "接尾相" # Suffix 2 - Need to clarify
    suffix3 = "接尾体" # Suffix 3 - Need to clarify
    assisting_particle = "副助" # Assisting particle
    counter = "助数" # Counter
    first_name = "名" # First name
    family_name = "姓" # Family name
    prefix = "接頭" # Prefix
    ending_particle = "終助" # Ending particle
    aspect = "相" # Aspect
    other = "他"


class UnidicGeneralString(UnidicField, str):
    """General string field for Unidic."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Validate the field as a general string."""
        return core_schema.no_info_after_validator_function(cls, handler(str))
    

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
    pos1: UnidicPos1 | None = Field(..., title="Part of Speech 1", description="The most general way of representing the part of speech.")
    pos2: UnidicPos2 | None = Field(..., title="Part of Speech 2", description="The second most general way of representing the part of speech.")
    pos3: UnidicPos3 | None = Field(..., title="Part of Speech 3", description="The third most general way of representing the part of speech.")
    pos4: UnidicPos4 | None = Field(..., title="Part of Speech 4", description="The most specific way of representing the part of speech.")
    cType: UnidicCType | None = Field(..., title="Conjugation Type", description="The type of conjugation.")
    cForm: UnidicCForm | None = Field(..., title="Conjugation Form", description="The form of conjugation.")
    lForm: str = Field(..., title="Lemma Form", description="The lemma form of the word.")
    lemma: str = Field(..., title="Lemma", description="The lemma of the word.")
    orth: str = Field(..., title="Orthography", description="The word as it appears in the text.")
    pron: str = Field(..., title="Pronunciation", description="The pronunciation of the word.")
    orthBase: str = Field(..., title="Base Orthography", description="The uninflected form of the word in context.")
    pronBase: str = Field(..., title="Base Pronunciation", description="The pronunciation of orthBase.")
    goshu: UnidicGoshu | None = Field(..., title="Goshu", description="The basic etymology of the word.")
    iType: UnidicGeneralString | None = Field(..., title="Initial Transformation", description="The type of initial transformation.")
    iForm: UnidicGeneralString | None = Field(..., title="Initial Form", description="The initial form of the word in context.")
    fType: UnidicGeneralString | None = Field(..., title="Final Transformation", description="The type of final transformation.")
    fForm: UnidicGeneralString | None = Field(..., title="Final Form", description="The final form of the word in context.")
    iConType: UnidicGeneralString | None = Field(..., title="Initial change fusion type", description="The type of initial change fusion.")
    fConType: UnidicGeneralString | None = Field(..., title="Final change fusion type", description="The type of final change fusion.")
    type: UnidicType | None = Field(..., title="Type", description="The type of the lemma.")
    kana: str = Field(..., title="Kana", description="The katakana representation of the word.")
    kanaBase: str = Field(..., title="Base Kana", description="The katakana representation of the lemma.")
    form: str = Field(..., title="Form", description="The form of the word.")
    formBase: str = Field(..., title="Base Form", description="The uninflected form of the word.")
    aType: str = Field(..., title="Accent Type", description="The accent type of the word.")
    aConType: str = Field(..., title="Accent change type", description="The accent change type of the word.")
    aModType: UnidicGeneralString | None = Field(..., title="Accent modification type", description="The accent modification type of the word.")
    lid: int = Field(..., title="Lexical ID", description="The lexical ID of the word. Mostly unique, except for half/full width versions of the same lemma.")
    lemma_id: int = Field(..., title="Lemma ID", description="The lemma ID of the word. Unique per lemma, but not per word.")

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
                pos1=UnidicPos1.from_fugashi(feature.pos1),
                pos2=UnidicPos2.from_fugashi(feature.pos2),
                pos3=UnidicPos3.from_fugashi(feature.pos3),
                pos4=UnidicPos4.from_fugashi(feature.pos4),
                cType=UnidicCType.from_fugashi(feature.cType),
                cForm=UnidicCForm.from_fugashi(feature.cForm),
                lForm=feature.lForm,
                lemma=feature.lemma,
                orth=feature.orth,
                pron=feature.pron,
                orthBase=feature.orthBase,
                pronBase=feature.pronBase,
                goshu=UnidicGoshu.from_fugashi(feature.goshu),
                iType=UnidicGeneralString.from_fugashi(feature.iType),
                iForm=UnidicGeneralString.from_fugashi(feature.iForm),
                fType=UnidicGeneralString.from_fugashi(feature.fType),
                fForm=UnidicGeneralString.from_fugashi(feature.fForm),
                iConType=UnidicGeneralString.from_fugashi(feature.iConType),
                fConType=UnidicGeneralString.from_fugashi(feature.fConType),
                type=UnidicType.from_fugashi(feature.type),
                kana=feature.kana,
                kanaBase=feature.kanaBase,
                form=feature.form,
                formBase=feature.formBase,
                aType=feature.aType,
                aConType=feature.aConType,
                aModType=UnidicGeneralString.from_fugashi(feature.aModType),
                lid=feature.lid,
                lemma_id=feature.lemma_id,
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

