if __name__ == '__main__':
    def transpose(x):
        return [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]


    def multiply(a, b):
        return [[sum(x * y for (x, y) in zip(row, col)) for col in b] for row in a]


    def scalar(n, m):
        return [[n if j == i else 0 for j in range(m)] for i in range(m)]


    def output(x):
        return "\n".join([" | ".join(f"{c:5}" for c in a) for a in x])


    A = [[10, -2, 8], [36, 7, -18], [3, 21, -11]]
    B = [[5], [0], [12]]
    B = transpose(B)
    C = multiply(A, B)
    # Your code goes here.

    print(output(C))
    print(output(multiply(A, scalar(2, len(A)))))
