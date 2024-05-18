import csv
from os.path import isfile


def get_words_and_scores_from_csv(file_path: str) -> list:

    # Items are stored in the csv as:
    # word,score[/n]word,score[\n]....
    word_list = []

    if not isfile(file_path):
        raise FileNotFoundError("word_scores missing")

    with open(file_path, 'r', encoding="utf8") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:

            if len(row) == 0:
                continue

            if len(row) == 2:  # Make this check more specific
                row.append(0)

            word, translated_word, score = row
            word_list.append([word, translated_word, float(score)])

    return word_list


def write_scores_to_csv(file_path: str, word_trans_score_list: list, edit_mode=False) -> None:

    # If want to just write the passed in list directly to csv
    if edit_mode:
        with open(file_path, 'w', encoding="utf-8") as f:
            csv_writer = csv.writer(f, delimiter=",", lineterminator="\n")
            csv_writer.writerows(word_trans_score_list)
        return

    csv_word_trans_score_list = get_words_and_scores_from_csv(
        file_path)

    # Inserts new values from word_trans_score_list into csv_list
    for word, trans, score in word_trans_score_list:
        for i, n in enumerate(csv_word_trans_score_list):
            csv_word, _, _ = n
            if csv_word == word:
                # update csv items of only selected words
                csv_word_trans_score_list[i] = [word, trans, score]

    with open(file_path, 'w', encoding="utf-8") as f:
        csv_writer = csv.writer(f, delimiter=",", lineterminator="\n")

        csv_writer.writerows(csv_word_trans_score_list)
