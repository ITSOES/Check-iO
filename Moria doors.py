import re


def count_score(word1, word2):
    return 10 * (word1[0] == word2[0]) + \
           10 * (word1[-1] == word2[-1]) + \
           30 * min(len(word1) / len(word2), len(word2) / len(word1)) + \
           50 * len(set(word1) & set(word2)) / len(set(word1) | set(word2))  # common over unique letters


def find_word(message):
    words = re.findall('[a-z]+', message.lower())[::-1]
    return max(words, key=lambda x: sum(count_score(compare, x) for compare in words))

print('asdcassa', find_word("Friend Fred and friend Ted."))
print(find_word("Speak friend and enter."))
if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert find_word("Speak friend and enter.") == "friend", "Friend"
    assert find_word("Beard and Bread") == "bread", "Bread is Beard"
    assert find_word("The Doors of Durin, Lord of Moria. Speak friend and enter. "
                     "I Narvi made them. Celebrimbor of Hollin drew these signs") == "durin", "Durin"
    assert find_word("Aoccdrnig to a rscheearch at Cmabrigde Uinervtisy."
                     " According to a researcher at Cambridge University.") == "according", "Research"
    assert find_word("One, two, two, three, three, three.") == "three", "Repeating"