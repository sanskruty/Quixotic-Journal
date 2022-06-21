import poem_model as pm


def predict(seed_text, seed):

    # seed_text = "Help me Obi Wan Kenobi, you're my only hope"
    # next_words = 100

    for _ in range(seed):
        token_list = pm.tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pm.pad_sequences([token_list], maxlen=pm.max_sequence_len - 1, padding='pre')
        with pm.graph.as_default():
            predicted = pm.model.predict_classes(token_list, verbose=0)
        output_word = ""
        for word, index in pm.tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
        # print(seed_text)

    return seed_text


# print(predict("Thy help"))