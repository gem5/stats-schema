
from json import load
import jsonschema
from pathlib import Path

def validate_instance(instance_path, schema, expect_valid = True):
    with open(instance_path) as f:
        instance = load(f)
    print(f"Testing {instance_path}")
    try:
        jsonschema.validate(instance, schema)
        if not expect_valid:
            print(f"{instance_path} FAILED!")
            print("Found valid instance.")
            return False
        else:
            print("SUCCESS")
            return True
    except jsonschema.exceptions.ValidationError as e:
        if expect_valid:
            print(f"{instance_path} FAILED!")
            print(e)
            return False
        else:
            print("SUCCESS")
            return True


def main():
    schema_file = '../simstats.schema.json'
    with open(schema_file) as f:
        schema = load(f)

    success = 0
    failed = 0
    skipped = 0

    for test_file in Path('examples/').glob('*.json'):
        if test_file.name.startswith('s-'):
            skipped += 1
            continue
        try:
            if validate_instance(test_file, schema,
                              expect_valid = test_file.name.startswith('v-')):
                success += 1
            else:
                failed += 1
        except jsonschema.exceptions.SchemaError as e:
            print(f"Schema file {schema_file} invalid.")
            return

    print(f"{success} succeeded {skipped} skipped and {failed} failed")

if __name__=="__main__":
    main()
