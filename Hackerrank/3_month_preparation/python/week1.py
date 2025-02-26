# test variables
arr = [1, 4, 10, 18]
s = "oieee"


def plus_minus(arr):
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

    def __init__(self):
        self.read_input()

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
                combined_words += words[index+1].upper()
                index +=1
            else:
                combined_words += words[index]
            index += 1

        return combined_words

    def read_line(self, line):
        if line[0]=="S":
            word = self.split(line[2])
        if line[0] == "C":
            word = self.combine(line[2])
            if line[1] =="M":
                word += "()"
            if line[1]=="C":
                word = word[0].upper() + word[1:]

        #Although word is possibly unbound, that is intentional to give an error
        #and I didn't care to treat error here
        print(word)

    def read_input(self):
        continue_loop = True
        number_of_loops = 0
        while continue_loop & number_of_loops <1e5:
            try:
                number_of_loops += 1
                line = input()
                line = line.strip().split(";")
                self.read_line(line)
            except EOFError:
                continue_loop = False
