import re

import requests


def parse_exam_file(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    # Split the text into questions using a regex to match "Question n:"
    questions = re.split(r"Question \d+:", text)

    parsed_questions = []
    for question in questions[
        1:
    ]:  # Skip the first element as it's before the first "Question n:"
        # Extract question text
        q_text_match = re.search(r"(.*?)(Answer \d+\.\d+:)", question, re.DOTALL)
        if q_text_match:
            q_text = q_text_match.group(1).strip()
        else:
            continue

        # Extract answers and explanation
        answers = re.findall(
            r"Answer \d+\.\d+: (.*?)(?=Answer \d+\.\d+:|Explanation \d+:|$)",
            question,
            re.DOTALL,
        )
        explanation_match = re.search(r"Explanation \d+: (.*)", question, re.DOTALL)

        if explanation_match:
            explanation = explanation_match.group(1).strip()
        else:
            explanation = ""

        parsed_answers = [ans.strip() for ans in answers]

        # Extract the correct answer from the extra field
        correct_answers = re.findall(r'CORRECT: "(.*?)"', explanation)
        clean_correct_answers = [
            ans.replace("(as explained above.)", "").strip() for ans in correct_answers
        ]
        correct_answer = "<br>".join(clean_correct_answers)

        parsed_questions.append((q_text, parsed_answers, correct_answer, explanation))

    return parsed_questions


def add_note_to_deck(
    deck_name, model_name, question, multiple_choice, correct_answer, extra
):
    # Format the multiple choice answers as bullet points
    formatted_choices = (
        "<ul>" + "".join(f"<li>{answer}</li>" for answer in multiple_choice) + "</ul>"
    )

    # Respect line breaks in the question and extra fields
    question = question.replace("\n", "<br>")
    extra = extra.replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;")

    note = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": model_name,
                "fields": {
                    "Question": question,
                    "Multiple Choice": formatted_choices,
                    "Correct Answer": correct_answer,
                    "Extra": extra,
                },
                "tags": [],
            }
        },
    }
    response = requests.post("http://localhost:8765", json=note)
    return response.json()


def main():
    file_path = "exams.txt"
    deck_name = "awsex"
    model_name = "Multiple Choice"

    # Parse the exam file
    parsed_questions = parse_exam_file(file_path)

    # Add each parsed question to the Anki deck
    for question, multiple_choice, correct_answer, extra in parsed_questions:
        response = add_note_to_deck(
            deck_name, model_name, question, multiple_choice, correct_answer, extra
        )
        print(response)


if __name__ == "__main__":
    main()
