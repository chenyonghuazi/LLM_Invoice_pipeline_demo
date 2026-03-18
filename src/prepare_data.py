import json
from pathlib import Path

# 1. this file's path
current_script = Path(__file__).resolve()

# 2. get this file's directory (src/)
current_dir = current_script.parent

# 3. look for parent directory (project/)
parent_dir = current_dir.parent

# 4. get target file path (config.ini in project/)
target_file = parent_dir / "labeled.json"


with open(target_file, 'r', encoding='utf-8') as f:
    tasks = json.load(f)

few_shot_examples = []
for task in tasks[:15]:  # the first 15 examples for few-shot demo
    text = task['data']['text']
    entities = {}
    if task.get('annotations'):
        for res in task['annotations'][0]['result']:
            if 'labels' in res['value']:
                label = res['value']['labels'][0]  # ex: "B-INVOICE_NUMBER"
                span = res['value']['text']
                # combine these key - value  pairs into a dictionary (key: value)
                key = label.replace('B-', '').replace('I-', '')
                entities[key] = entities.get(key, '') + ' ' + span
    few_shot_examples.append({
        "input_text": text[:300] + "..." if len(text) > 300 else text,
        "output": entities
    })

# 4. get target file path (config.ini in project/)
target_save_file = parent_dir / "few_shot_examples.json"

# save this file
with open(target_save_file, 'w', encoding='utf-8') as f:
    json.dump(few_shot_examples, f, ensure_ascii=False, indent=2)

print("Done preparing few-shot examples. Saved to few_shot_examples.json")

# 5. get target file path (config.ini in project/)
target_test_file = parent_dir / "invoices.json"

test_example = []
with open(target_test_file, 'r', encoding='utf-8') as f:
    test_example = json.load(f)
    
# print(f"\n loaded test example: {test_example[14:]}")
    