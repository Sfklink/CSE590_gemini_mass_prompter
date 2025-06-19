import os
import json
import re

def clean_text_value(text: str, to_remove: list[str]) -> str:
    for pattern in to_remove:
        text = re.sub(pattern, '', text)
    return text

def recursively_clean(obj, to_remove):
    """
    Recursively clean all string values in the JSON object.
    """
    if isinstance(obj, dict):
        return {k: recursively_clean(v, to_remove) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursively_clean(elem, to_remove) for elem in obj]
    elif isinstance(obj, str):
        return clean_text_value(obj, to_remove)
    else:
        return obj

def merge_json_to_txt(folder_path: str, output_file: str) -> None:
    to_remove = [
        r'\\n',            # literal "\n"
        r'\n',
        r'\\"',            # literal '\"'
        r'\\n\\n',
        r'\\u2013',        # en-dash
        r'\*{1,2}',        # * and **
        r'\\u00a7',
        r'\\'
    ]

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.json') and 'responses' in filename:
                json_path = os.path.join(folder_path, filename)
                with open(json_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        cleaned_data = recursively_clean(data, to_remove)
                        json.dump(cleaned_data, outfile, indent=2, ensure_ascii=False)
                        outfile.write('\n\n')
                    except json.JSONDecodeError as e:
                        print(f"Skipping {filename}: Invalid JSON - {e}")

    print(f"Cleaned JSON contents written to: {output_file}")

if __name__ == "__main__":
    folder = "./prompts+responses"
    output = "./prompts+responses/merged_response_output.txt"
    merge_json_to_txt(folder, output)
