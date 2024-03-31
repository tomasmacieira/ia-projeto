# Bimaru Solver

## Introduction
This project for the Artificial Intelligence (AI) course develops a Python program that solves the Bimaru problem using AI techniques. Bimaru,
also known as Battleship Puzzle, Yubotu, or Solitaire Battleship, is a puzzle inspired by the well-known Battleship game between two players. 

## Problem Description
According to the description provided in CSPlib, the Bimaru game takes place on a square grid representing an area of the ocean. Typically, published games use a 10x10 grid, which we'll assume for this project.
The ocean area contains a hidden fleet that the player must find, consisting of one battleship (four squares in length), two cruisers (each with three squares in length),
three destroyers (each with two squares in length), and four submarines (one square each). Ships can be oriented horizontally or vertically, and no two ships occupy adjacent squares on the grid,
even diagonally. The player also receives row and column counts, indicating the number of occupied squares in each row and column,
along with various hints specifying the state of individual squares on the grid. <br><br>

![Example of a Bimaru instance](https://github.com/tomasmacieira/ia-projeto/blob/master/imgs/Fig1.png)  
Figure 1: Example of a Bimaru instance<br><br>

![Example of a Bimaru instance](https://github.com/tomasmacieira/ia-projeto/blob/master/imgs/Fig2.png)  
Figure 2: Example of a solution for a Bimaru instance<br><br>



## Usage

To solve a Bimaru instance, run the following command (you can find instances in the `instances` folder):

```bash
python3 bimaru.py < <instance_file>
```

Alternatively, you can run the tester script by executing:
```bash
python3 Tests/Tester/tester.py
```
Which will execute all the instances in the `tests` folder and put the outputs in the `my_outputs` folder.

### Input Format

Bimaru problem instances consist of 3 parts:

1. The first line starts with the word ROW and contains information regarding the count of occupied positions in each row of the grid.
2. The second line starts with the word COLUMN and contains information regarding the count of occupied positions in each column of the grid.
3. The third line contains an integer corresponding to the number of hints.
4. The following lines start with the word HINT and contain hints corresponding to pre-filled positions.

Formally, each of the 4 parts described above has the following format:
1. ROW \<count-0> ... \<count-9>
2. COLUMN \<count-0> ... \<count-9>
3. \<hint total>
4. HINT \<row> \<column> \<hint value>

Possible values for \<row> and \<column> are integers between 0 and 9. The upper-left corner of the grid corresponds to coordinates (0,0).

Possible values for \<hint value> are: W (water), C (circle), T (top), M (middle), B (bottom), L (left), and R (right).

### Example

The input file describing the instance in Figure 1 is as follows:

```plaintext
ROW 2 3 2 2 3 0 1 3 2 2
COLUMN 6 0 1 0 2 1 3 1 2 4
6
HINT 0 0 T
HINT 1 6 M
HINT 3 2 C
HINT 6 0 W
HINT 8 8 B
HINT 9 5 C

ROW\t2\t3\t2\t2\t3\t0\t1\t3\t2\t2\n
COLUMN\t6\t0\t1\t0\t2\t1\t3\t1\t2\t4\n
6\n
HINT\t0\t0\tT\n
HINT\t1\t6\tM\n
HINT\t3\t2\tC\n
HINT\t6\t0\tW\n
HINT\t8\t8\tB\n
HINT\t9\t5\tC\n
```

### Output Format

The output of the program should describe a solution to the Bimaru problem described in the input file, i.e., a fully filled grid that respects the previously stated rules. The output should follow the following format:
- 10 lines, where each line indicates the content of the respective grid row.
- Uppercase letters are used for pre-filled positions (hints).
- Lowercase letters are used for other positions, except for water positions, which are represented by a period for readability.
- Each line, including the last one, should be terminated by the newline character (\n).

### Example

The output describing the solution to Figure 2 is as follows:

```plaintext
T.....t...
b.....M..t
......b..m
..C......m
c......c.b
..........
W...t.....
t...b...t.
m.......B.
b....C....

T.....t...\n
b.....M..t\n
......b..m\n
..C......m\n
c......c.b\n
..........\n
W...t.....\n
t...b...t.\n
m.......B.\n
b....C....\n
```
