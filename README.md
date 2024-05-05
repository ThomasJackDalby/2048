# 2048 Solver

A quick & dirty 2048 solver written at a hackathon.

The general premise is to read the grid based on the colours of the tiles (thankfully each numeric tile has a slightly different background hue).

Then, doing various degrees of lookahead, chooses the direction that will minimise the overall score of the grid.

Written in Python using pyautogui.