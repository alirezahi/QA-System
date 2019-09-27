def freq(string_arr):
    result = []
    for word in set(string_arr):
        result.append((word, string_arr.count(word)))
    return result

def freq_count(string, freq_number):
    result = 0
    for (word, count) in freq(string):
        if count == freq_number:
            result += 1
    return result


# شمارش تعداد واژههای با بسامد ١ در هر متن
def words_frequency_one(words):
    great_string = []
    for word in words:
        great_string.append(word['wordForm'])
    result = freq_count(great_string, 1)
    return result
