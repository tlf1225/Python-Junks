if __name__ == '__main__':
    TRANSPOSE = lambda x: [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
    MULTIPLY = lambda a, b: [[sum(x * y for (x, y) in zip(row, col)) for col in b] for row in a]
    SCALAR = lambda n, m: [[n if j == i else 0 for j in range(m)] for i in range(m)]
    OUTPUT = lambda x: "\n".join([" | ".join(f"{c:5}" for c in a) for a in x])

    A = [[10, -2, 8], [36, 7, -18], [3, 21, -11]]
    B = [[5], [0], [12]]
    B = TRANSPOSE(B)
    C = MULTIPLY(A, B)
    # Your code goes here.

    print(OUTPUT(C))
    print(OUTPUT(MULTIPLY(A, SCALAR(2, len(A)))))
