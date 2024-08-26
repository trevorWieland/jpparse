"""scratch file."""

import json

from jpparse import ScriptParser
from jpparse.types import ScriptIndex

with open("data/index.json", "r", encoding="utf-8") as f:
    index = ScriptIndex.model_validate_json(f.read())

target_vn = "leyline1"

metadata = next(script for script in index.scripts if script.name == target_vn)

parser = ScriptParser.from_metadata(metadata, "data/scripts", analysis_mode=True)

parsed_script = parser.parse()

analysis_dict = {k: sorted(list(v)) for k,v in parser.analysis_dict.items()}

with open("analysis.json", "w", encoding="utf-8") as f:
    json.dump(analysis_dict, f, indent=4)