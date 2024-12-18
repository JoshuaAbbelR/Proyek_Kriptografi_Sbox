import numpy as np

def validate_sbox(s_box):
    """Validasi apakah S-Box memiliki panjang 256 dan elemen unik."""
    if len(s_box) != 256:
        return False, "Panjang S-Box bukan 256."
    if len(set(s_box)) != 256:
        return False, "S-Box memiliki elemen duplikat."
    return True, "S-Box valid."

def hamming_weight(x):
    return bin(x).count('1')

def truth_table(sbox, n, m):
    table = []
    for i in range(m):
        column = [(sbox[x] >> i) & 1 for x in range(2**n)]
        column = [2 * val - 1 for val in column]
        table.append(column)
    return np.array(table)

def walsh_transform(column):
    n = len(column)
    W = np.array(column)
    for i in range(int(np.log2(n))):
        half = 2**i
        for j in range(0, n, 2 * half):
            for k in range(half):
                a = W[j + k]
                b = W[j + k + half]
                W[j + k] = a + b
                W[j + k + half] = a - b
    return W

def nonlinearity(sbox, n, m):
    table = truth_table(sbox, n, m)
    min_distance = float('inf')
    for column in table:
        W = walsh_transform(column)
        max_walsh = np.max(np.abs(W))
        distance = 2**(n - 1) - max_walsh / 2
        min_distance = min(min_distance, distance)
    return int(min_distance)

def sac(sbox, n):
    total = 0
    for i in range(2**n):
        original = sbox[i]
        for bit in range(n):
            flipped_input = i ^ (1 << bit)
            flipped_output = sbox[flipped_input]
            diff = original ^ flipped_output
            total += hamming_weight(diff)
    return total / (n * 2**n * n)

def bic_nl(sbox, n):
    total_nl = 0
    count = 0
    for bit1 in range(n):
        for bit2 in range(bit1 + 1, n):
            count += 1
            sbox_bit1 = [(x >> bit1) & 1 for x in sbox]
            sbox_bit2 = [(x >> bit2) & 1 for x in sbox]
            combined = [2 * (b1 ^ b2) - 1 for b1, b2 in zip(sbox_bit1, sbox_bit2)]
            W = walsh_transform(combined)
            max_walsh = np.max(np.abs(W))
            total_nl += 2**(n - 1) - max_walsh / 2
    return int(total_nl / count)

def lap(sbox, n):
    max_bias = 0
    for a in range(1, 2**n):
        for b in range(1, 2**n):
            bias = 0
            for x in range(2**n):
                input_parity = hamming_weight(x & a) % 2
                output_parity = hamming_weight(sbox[x] & b) % 2
                if input_parity == output_parity:
                    bias += 1
            bias = abs(bias - 2**(n - 1))
            max_bias = max(max_bias, bias / 2**n)
    return max_bias

def dap(sbox, n):
    max_diff_prob = 0
    for dx in range(1, 2**n):
        for dy in range(1, 2**n):
            count = 0
            for x in range(2**n):
                if sbox[x ^ dx] ^ sbox[x] == dy:
                    count += 1
            prob = count / 2**n
            max_diff_prob = max(max_diff_prob, prob)
    return max_diff_prob