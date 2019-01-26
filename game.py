from enum import Enum

from board import *



if __name__ == "__main__":
    board = construct_board()

    score = []
    for i in range(52):
        pts = board.features[i].value('RED')
        value = pts[0]/36.0 * sum(pts[1:])
        score.append((i, value, pts))

    score.sort(key=lambda x: x[1], reverse=True)

    for each in score:
        print(each)