from fractions import Fraction

DEV = True

sample_text = """4
1 3
FFT 3
1 3
FFT 2
2 6
FFTTTF 2
FTFTFT 4
2 2
FF 1
TT 1
"""


if DEV:
    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    test_cases = []
    for t in range(n_test_cases):
        N, Q = list(map(int, input().split()))
        students = []
        for student_i in range(N):
            A, S = list(input().split())
            students.append((A, int(S)))

        yield (N, Q, students)


def hacked_exam(N, Q, students):
    question_scores = [[0,0] for _ in range(Q)] # T, F
    print()
    print(N, Q, students)

    for answers, score in students:
        for i in range(Q):
            if answers[i] == "T":
                question_scores[i][0] += Fraction(score, Q)
                question_scores[i][1] += Fraction(Q-score, Q)
            else:
                question_scores[i][0] += Fraction(Q-score, Q)
                question_scores[i][1] += Fraction(score, Q)

    print("Trues: {}".format([x[0] for x in question_scores]))
    print("Falses: {}".format([x[1] for x in question_scores]))
    my_answers = []
    my_score = Fraction(0)

    for i in range(Q):
        T, F = question_scores[i]
        if T > F:
            my_answers.append("T")
            my_score += T
        else:
            my_answers.append("F")
            my_score += F

    my_score /= N


    ans_str = "".join(my_answers)
    score_str = str(my_score.numerator) + "/" + str(my_score.denominator)
    return ans_str+  " " + score_str 




def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, hacked_exam(*test_case)))

if __name__ == '__main__':
    main()
