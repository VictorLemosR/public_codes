# test variables
arr = [1, 4, 10, 18]
s = "oieee"


def plus_minus(arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    len_arr = len(arr)
    positive_numbers = 0
    negative_numbers = 0
    for number in arr:
        if number > 0:
            positive_numbers += 1
        elif number < 0:
            negative_numbers += 1

    print(round(positive_numbers / len_arr, 6))
    print(round(negative_numbers / len_arr, 6))
    print(round((len_arr - positive_numbers - negative_numbers) / len_arr, 6))


def mini_max_sum(arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    sum = 0
    minimum_number = arr[0]
    maximum_number = arr[0]
    for number in arr:
        sum += number
        if number < minimum_number:
            minimum_number = number
        if number > maximum_number:
            maximum_number = number

    print("{sum - maximum_number} {sum - minimum_number}")


def time_conversion(s):
    # s has a fixed length
    # Time complexity: O(1)
    # Space complexity (ignoring input): O(1)
    s_len = len(s)
    hour = s[0:2]
    am_pm = s[s_len - 2 :]
    if hour == "12":
        if am_pm == "AM":
            hour = "00"
        else:
            hour = "12"
    elif am_pm == "PM":
        hour = str(int(hour) + 12)

    return hour + s[2 : (s_len - 2)]


def breaking_the_records(scores):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    minimum = scores[0]
    maximum = scores[0]
    records = [0, 0]
    for index in range(1, len(scores)):
        score = scores[index]
        print(score, minimum, maximum)
        if score < minimum:
            minimum = score
            records[0] += 1
        if score > maximum:
            maximum = score
            records[1] += 1

    return records


class CamelCase:
    # n being the length of the words
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(n)

    def __init__(self):
        self.read_input()

    def read_input(self):
        continue_loop = True
        number_of_loops = 0
        while continue_loop & number_of_loops < 1e5:
            try:
                number_of_loops += 1
                line = input()
                line = line.strip().split(";")
                self.read_line(line)
            except EOFError:
                continue_loop = False

    def read_line(self, line):
        if line[0] == "S":
            word = self.split(line[2])
        if line[0] == "C":
            word = self.combine(line[2])
            if line[1] == "M":
                word += "()"
            if line[1] == "C":
                word = word[0].upper() + word[1:]

        # Although word is possibly unbound, that is intentional to give an error
        # and I didn't care to treat error here
        print(word)

    def split(self, word: str):
        if word.endswith("()"):
            word = word[:-2]
        splitted_word = word[0].lower()
        word = word[1:]
        for letter in word:
            if letter.upper() == letter:
                splitted_word += " " + letter.lower()
            else:
                splitted_word += letter

        return splitted_word

    def combine(self, words):
        combined_words = ""
        index = 0
        while index < len(words):
            letter = words[index]
            if letter == " ":
                combined_words += words[index + 1].upper()
                index += 1
            else:
                combined_words += words[index]
            index += 1

        return combined_words

def divisible_sum_pairs(n: int, k: int, ar: list[int]):
    #Time complexity: O(n+k)
    #Space complexity (ignoring input): O(k)
    possible_remainders = {}
    total_pairs = 0

    for number in ar:
        remainder = number % k
        if remainder in possible_remainders:
            possible_remainders[remainder] += 1
        else:
            possible_remainders[remainder] = 1

    # For remainder 0 or k/2, the total pairs will be n choose 2
    if 0 in possible_remainders:
        total_pairs += int(possible_remainders[0] * (possible_remainders[0] - 1) / 2)
    k_is_pair = k % 2 == 0
    half_k = int(k / 2)
    if k_is_pair and (half_k in possible_remainders):
        total_pairs += int(
            possible_remainders[half_k] * (possible_remainders[half_k] - 1) / 2
        )

    # For the rest of the remainders, just need to multiply
    for remainder in range(1, int((k + 1) / 2)):
        if (remainder in possible_remainders) and (
            (k - remainder) in possible_remainders
        ):
            total_pairs += int(
                possible_remainders[remainder] * (possible_remainders[k - remainder])
            )

    return total_pairs

def sparse_arrays(strings, queries):
    #Time complexity: O(n+m)
    #Space complexity (ignoring input): O(n+m)
    strings_dictionary = {}

    for string in strings:
        if string in strings_dictionary:
            strings_dictionary[string] += 1
        else:
            strings_dictionary[string] = 1

    strings_found = []
    for query in queries:
        if query in strings_dictionary:
            strings_found.append(strings_dictionary[query])
        else:
            strings_found.append(0)

    return strings_found
