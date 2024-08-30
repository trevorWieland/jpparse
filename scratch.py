"""scratch file."""

import json

from jpparse import ScriptParser
from jpparse.types import ScriptIndex

with open("data/index.json", "r", encoding="utf-8") as f:
    index = ScriptIndex.model_validate_json(f.read())

analysis_dict = {}
for metadata in index.scripts[:1]:
    print(f"Processing {metadata.name}...")

    parser = ScriptParser.from_metadata(metadata, "data/scripts", analysis_mode=True)

    if len(parser.analysis_dict.keys()) == 0:
        parser.analysis_dict = analysis_dict

    parsed_script = parser.parse()

    with open(f"data/parsed/{metadata.name}.json", "w", encoding="utf-8") as f:
        f.write(parsed_script.model_dump_json(indent=4))

    analysis_dict = parser.analysis_dict

analysis_dict = {k: sorted(list(v)) for k, v in analysis_dict.items()}

with open("analysis.json", "w", encoding="utf-8") as f:
    json.dump(analysis_dict, f, indent=4)
