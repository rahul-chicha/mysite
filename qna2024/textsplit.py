import re
import json

def extract_info(input_string):
    # Define a pattern to capture different sections
    print(input_string)
    pattern = re.compile(r'(\d+\.)\s*\*\s*(.*?)(?:\((A|B|C|D|E)\)\s*(.*?)(?=\([A-E]\)|\[|$))?\s*(\[.*?\])?\s*(.*)')

    # Extract information using the pattern
    match = pattern.match(input_string)
    print(match)
    output_data = {}

    if match:
        output_data["QuestionNumber"] = match.group(1)
        output_data["QuestionText"] = match.group(2)

        options = match.group(3)
        option_descriptions = match.group(4)

        if options and option_descriptions:
            output_data["Options"] = [(opt, desc) for opt, desc in zip(options, option_descriptions)]
        else:
            output_data["Options"] = []

        output_data["AnswerKey"] = match.group(5) if match.group(5) else ""
        output_data["ExamName"] = match.group(6) if match.group(6) else ""
        output_data["AnswerDescription"] = match.group(7) if match.group(7) else ""
    #output_json = json.dumps(extract_info(example_string), ensure_ascii=False, indent=2)
    return output_data