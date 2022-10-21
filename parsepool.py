import argparse
import json
from os.path import exists

def main():
    parser = argparse.ArgumentParser(description='Converts NCVEC Amateur Radio question pools into JSON files.')
    parser.add_argument("-i", "--input", help="Filename of question pool to be inported", required=True)
    parser.add_argument("-o", "--output", help="Directs the JSON to a name of your choice", required=True)
    args = parser.parse_args()

    file = open(str(args.input), "r", encoding="utf-8")
    pool = file.read()
    file.close()

    output_pool = []

    for question in pool.split("\n\n"):   # split question pool into individual questions
        if question.count("\n") > 3:
            question_dict = {
                "id": "",
                "correct": "",
                "question": "",
                "answers": ""
            }
            qlines = question.split("\n")       # split questions into lines
            ## FIRST LINE: Question ID and Correct Answer
            qline1 = qlines[0].split(" ")
            qid = qline1[0]                     # question ID ## IMPORTANT!!!
            answer_letter = qline1[1]           # correct answer
            answer_num = None                   # for checking
            for i in range(0, 4):               # convert letter to index (0-3)
                if ord(answer_letter[1]) == 65 + int(i):
                    answer_num = i
                    break
            if answer_num == None:
                print("ERROR: I couldn't parse the answer letter to a number. :(")
                exit()
            ## SECOND LINE: Written Question
            written_question = qlines[1]
            ## Answers
            answers = []
            for i in range(0, 4):
                answers.append(qlines[i + 2][3:])
            
            # append to question dictionary
            question_dict["id"] = qid
            question_dict["correct"] = answer_num
            question_dict["question"] = written_question
            question_dict["answers"] = answers

            output_pool.append(question_dict)

    with open(str(args.output), 'w', encoding='utf-8') as filename:
        json.dump(output_pool, filename, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()


        
