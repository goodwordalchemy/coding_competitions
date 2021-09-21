from fractions import Fraction

DEV = True

sample_text = """5
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
3 120
FFTFFFTFFFTTTTTTTFTFFFFFFTTTFTFFFTFTFFTTFTFFTFFTTTFTFTFFTFTFTTFFFFTFTFFFFTTTFTTFTTTTFFFTTFFFFFTTFFTFFTFFTTTFFFFTTFFTFTTF 55
FFFTFFTTFFFFTFTFFTFFFTTTTTTFFFTTTFTTTTFFTFTTTFTTFFTTTFTFFFFTFFTTFFTTFTTFFTFTFFTFTTFTFTFFTTTFFTFTFTTFFTFTFTFTTFFTFFFTFTFT 62
FFFTFTTFFFFFTFTFTTTTTTFFTTFTFFFTFFTTTTTTFFFTTTFFFTTFTFFFFFFTFTTFFTFTTTFTTTTFTTFFFFTFFTTFTFFTTTTTTFTFFFFFTTFFTFTFTFFTTTTT 64
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
    question_scores = [[0,0,0,0] for _ in range(Q)] # T, F
    print()
    print(N, Q, students)

    for answers, score in students:
        for i in range(Q):
            if answers[i] == "T":
                question_scores[i][0] += score
                question_scores[i][1] += Q-score
                question_scores[i][2] += 1
            else:
                question_scores[i][0] += Q-score
                question_scores[i][1] += score
                question_scores[i][3] += 1

    print("Trues: {}".format([x[0] for x in question_scores]))
    print("Falses: {}".format([x[1] for x in question_scores]))
    my_answers = []
    my_score = Fraction(0)

    for i in range(Q):
        T, F, Tc, Fc = question_scores[i]
        if T > F:
            my_answers.append("T")
            my_score += Fraction(1, 2) + (Fraction(T,  N) - Fraction(1, 2))
        else:
            my_answers.append("F")
            my_score += Fraction(1, 2) +  (Fraction(F , N) - Fraction(1, 2))

    my_score /= Q


    ans_str = "".join(my_answers)
    score_str = str(my_score.numerator) + "/" + str(my_score.denominator)
    return ans_str+  " " + score_str 




def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, hacked_exam(*test_case)))

if __name__ == '__main__':
    main()
