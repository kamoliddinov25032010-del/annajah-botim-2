import random

from games.beginner import questions as beginner
from games.elementary import questions as elementary
import random

from games.beginner import questions as beginner
from games.elementary import questions as elementary


def get_shuffled_questions(level="beginner"):

    if level == "beginner":
        questions = beginner
    else:
        questions = elementary

    shuffled = []

    for q in questions:
        answers = q["answers"].copy()

        correct_answer = answers[
            ["A", "B", "C", "D"].index(q["correct"])
        ]

        random.shuffle(answers)

        new_correct = ["A", "B", "C", "D"][answers.index(correct_answer)]

        shuffled.append({
            "question": q["question"],
            "answers": answers,
            "correct": new_correct
        })

    random.shuffle(shuffled)

    return shuffled


def get_duel_questions(count=5):
    pool = beginner + elementary
    selected = random.sample(pool, min(count, len(pool)))

    shuffled = []

    for q in selected:
        answers = q["answers"].copy()

        correct_answer = answers[
            ["A", "B", "C", "D"].index(q["correct"])
        ]

        random.shuffle(answers)

        new_correct = ["A", "B", "C", "D"][answers.index(correct_answer)]

        shuffled.append({
            "question": q["question"],
            "answers": answers,
            "correct": new_correct
        })

    return shuffled