#!/usr/bin/env python3
"""One Letter: Coffee or Tea.

The brief: send exactly one letter and nothing else. ``A`` for coffee,
``B`` for tea. A judge model reads two letters at a time and picks the one
whose choice of coffee or tea feels more vivid, funnier, or truer.

This program makes that choice deliberately, then writes the single letter
to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` -- one UTF-8 character, no newline,
no punctuation, nothing else. It is fully deterministic: no clock, no
randomness, no network, no input files.
"""

import os
import sys

# The judge's criteria, in the order the brief lists them, with the
# reasoning that decides each one. Scores are out of 5; the drink with the
# higher total wins the letter.
CRITERIA = (
    # Vivid: which choice lands as the fuller, more alive answer?
    # Coffee is dark, steaming, bitter, loud -- a drink you can smell from
    # the doorway. Tea is gentle and quiet by comparison.
    ("vivid", "coffee", "tea", 5, 3),
    # Funny: which choice carries more wit or surprise?
    # Coffee owns the whole caffeine-dependence joke canon -- "don't talk
    # to me before my coffee", the fourth cup, the trembling hand. Tea's
    # jokes are polite; coffee's are confessions.
    ("funny", "coffee", "tea", 5, 2),
    # True: which choice is the more honest answer for the person sending
    # it? The morning ritual most people actually live by -- the pot
    # brewing before the day starts, the cup that gets them to work -- is
    # coffee. Tea is the aspiration; coffee is the habit.
    ("true", "coffee", "tea", 4, 3),
)


def score_drink(drink, criteria=CRITERIA):
    """Total the judge's criterion scores for one drink."""
    total = 0
    for _name, first, second, first_score, second_score in criteria:
        if first == drink:
            total += first_score
        elif second == drink:
            total += second_score
    return total


def decide(criteria=CRITERIA):
    """Weigh coffee against tea on the judge's criteria.

    Returns "A" for coffee or "B" for tea.
    """
    coffee = score_drink("coffee", criteria)
    tea = score_drink("tea", criteria)
    # Coffee 14, tea 8. Coffee wins on vividness and humour by a clear
    # margin and holds truth as the daily ritual -- so the letter is A.
    if coffee >= tea:
        return "A"
    return "B"


def main():
    letter = decide()
    assert letter in ("A", "B") and len(letter) == 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Exactly one character: no newline, no trailing space.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(letter)

    # Self-check: the file must hold one non-whitespace character.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if len(written) != 1 or written.isspace():
        print(f"entry.txt must hold exactly one letter, got {written!r}",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
