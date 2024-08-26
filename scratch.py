"""scratch file."""

import json

from jpparse import ScriptParser
from jpparse.types import ScriptIndex

with open("data/index.json", "r", encoding="utf-8") as f:
    index = ScriptIndex.model_validate_json(f.read())

target_vns = ["leyline1", "leyline2", "leyline3"]

analysis_dict = {}
for target_vn in target_vns:
    print(f"Processing {target_vn}...")
    metadata = next(script for script in index.scripts if script.name == target_vn)

    parser = ScriptParser.from_metadata(metadata, "data/scripts", analysis_mode=True)

    if len(parser.analysis_dict.keys()) == 0:
        parser.analysis_dict = analysis_dict

    parsed_script = parser.parse()

    analysis_dict = parser.analysis_dict

analysis_dict = {k: sorted(list(v)) for k,v in analysis_dict.items()}

with open("analysis.json", "w", encoding="utf-8") as f:
    json.dump(analysis_dict, f, indent=4)