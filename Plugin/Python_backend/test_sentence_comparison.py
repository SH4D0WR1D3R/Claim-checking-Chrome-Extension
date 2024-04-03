import evidence_sentence_comparison
import sentence_comparison

with open('sentence_comparison_test_sentences.txt', 'r') as file:
    test_sentences = file.readlines()
    # print("Test sentences: ", test_sentences)
    sentence_comparison_object = sentence_comparison.sentence_comparison()
    for pair in test_sentences:
        pair = pair.split(" SEPARATOR ")
        print(pair)
        print(sentence_comparison_object.sentences_agree(pair[0], pair[1]))



