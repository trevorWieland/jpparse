"""scratch file."""


from jpparse import ScriptParser
from jpparse.types import ScriptIndex

with open("data/index.json", "r", encoding="utf-8") as f:
    index = ScriptIndex.model_validate_json(f.read())

for metadata in index.scripts:
    print(f"Processing {metadata.name}...")

    try:
        parser = ScriptParser.from_metadata(metadata, "data/scripts", analysis_mode=False)
    except FileNotFoundError:
        print(f"Script {metadata.name} not found.")
        continue

    parsed_script = parser.parse()

    with open(f"data/parsed/{metadata.name}.json", "w", encoding="utf-8") as f:
        f.write(parsed_script.model_dump_json(indent=4))

