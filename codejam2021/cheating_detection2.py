import math


DEV = False

input = raw_input
if DEV:
    with open("cheating_detection_sample_input.txt", "r") as handle:
        sample_text = handle.read()

    from collections import deque
    from unittest.mock import MagicMock
    sample_lines = deque(sample_text.split("\n"))

    input = MagicMock(side_effect=lambda : sample_lines.popleft())



def parse_input():
    n_test_cases = int(input())
    p = int(input())
    for t in range(n_test_cases):
        data = []
        for _ in range(100):
            data.append(input())

        yield data

M_students = 100
N_questions = 10000


def sigmoid(x):
      return 1 / (1 + math.exp(-x))

def project_to_range_3(x):
    return 6 * x - 3

def argmax(L):
    best_val = -float('inf')
    best_idx = -1
    for idx, val in enumerate(L):
        if val > best_val:
            best_val = val
            best_idx = idx
    return best_idx

def cheating_detection(data):
    difficulties = [0] * N_questions
    skills = [0] * M_students

    for i, student in enumerate(data):
        for j, is_correct in enumerate(student):
            skills[i] += int(is_correct)
            difficulties[j] += int(is_correct)

    for i in range(len(skills)):
        skills[i] = project_to_range_3(skills[i] / N_questions)

    for j in range(len(difficulties)):
        difficulties[j] = project_to_range_3(difficulties[j] / M_students)

    surprise = [0] * M_students

    for i, student in enumerate(data):
        for j, is_correct in enumerate(student):
            if not int(is_correct):
                continue
            surprise[i] += 1 - sigmoid(skills[i] - difficulties[j])
        surprise[i] *= skills[i]**2

    if DEV:
        print("diff...")
        print(difficulties)
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2)
        axes[0].hist(difficulties, bins=100)
        axes[0].set_title("diff")
        
        print("skill...")
        print(skills)
        axes[1].hist(skills, bins=100)
        axes[1].set_title("skill")

        plt.show()

        for s, i in sorted(((s, i+1) for i, s in enumerate(surprise)), reverse=True):
            print(s, i)
    return argmax(surprise) + 1

        



def main():
    for i, test_case in enumerate(parse_input()):
        print("Case #{}: {}".format(i+1, cheating_detection(test_case)))

if __name__ == '__main__':
    main()
