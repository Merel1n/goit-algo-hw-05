from timeit import timeit

def read_file(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No such file: {filename}") from e
    except PermissionError as e:
        raise PermissionError(f"Permission denied: {filename}") from e
    except Exception as e:
        raise Exception(f"Error reading {filename}") from e
    
def kmp_search(text, pattern):
    lps = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def bm_search(text, pattern):
    m, n = len(pattern), len(text)
    if m > n:
        return -1

    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}

    i = m - 1
    while i < n:
        k = 0
        while k < m and pattern[m - 1 - k] == text[i - k]:
            k += 1
        if k == m:
            return i - m + 1
        i += skip.get(text[i], m)
    return -1


def rabin_karp(text, pattern):
    m, n = len(pattern), len(text)
    if m > n:
        return -1

    base = 256
    mod = 10 ** 9 + 7

    hash_p = 0
    hash_t = 0
    power = 1

    for i in range(m - 1):
        power = (power * base) % mod

    for i in range(m):
        hash_p = (hash_p * base + ord(pattern[i])) % mod
        hash_t = (hash_t * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if hash_p == hash_t:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            hash_t = (hash_t - ord(text[i]) * power) % mod
            hash_t = (hash_t * base + ord(text[i + m])) % mod

    return -1

existing_sub1 = "index"
fake_sub1 = "qwertyuiop123"

existing_sub2 = "данних"
fake_sub2 = "abracadabraXYZ"

def measure(text, pattern):
    return {
        "BM": timeit(lambda: bm_search(text, pattern), number=50),
        "KMP": timeit(lambda: kmp_search(text, pattern), number=50),
        "RK": timeit(lambda: rabin_karp(text, pattern), number=50)
    }



def main():
    try:
        text1 = read_file("memoir_1.txt")
        text2 = read_file("memoir_2.txt")
    except Exception as e:
        print(f"⚠️ Error from {type(e).__name__}: {e}")
        exit(1)

    print("=== ARTICLE 1 ===")
    print("Existing:", measure(text1, existing_sub1))
    print("Fake:", measure(text1, fake_sub1))

    print("\n=== ARTICLE 2 ===")
    print("Existing:", measure(text2, existing_sub2))
    print("Fake:", measure(text2, fake_sub2))

if __name__ == "__main__":
    main()