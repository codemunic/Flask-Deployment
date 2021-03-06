from model.data_utils import CoNLLDataset
from model.config import Config
from model.ner_model import NERModel
from model.ner_learner import NERLearner
import sys

def align_data(data):
    """Given dict with lists, creates aligned strings
    Adapted from Assignment 3 of CS224N
    Args:
        data: (dict) data["x"] = ["I", "love", "you"]
              (dict) data["y"] = ["O", "O", "O"]
    Returns:
        data_aligned: (dict) data_align["x"] = "I love you"
                           data_align["y"] = "O O    O  "
    """
    spacings = [max([len(seq[i]) for seq in data.values()])
                for i in range(len(data[list(data.keys())[0]]))]
    data_aligned = dict()

    # for each entry, create aligned string
    for key, seq in data.items():
        str_aligned = ""
        for token, spacing in zip(seq, spacings):
            str_aligned += token + " " * (spacing - len(token) + 1)

        data_aligned[key] = str_aligned

    return data_aligned

def get_model_api():
    """Returns lambda function for api"""
    # 1. initialize model once and for all and reload weights
    config = Config(load=True)
    config.processing_word = None
    model  = NERModel(config)
    learn = NERLearner(config, model)
    learn.load()

    def model_api(input_data):
        #if input_data is None:
        if not input_data:
            input_data = "Trump is yet to visit New Delhi."

        # 2. process input with simple tokenization and no punctuation
        punc = [",", "?", ".", ":", ";", "!", "(", ")", "[", "]"]
        s = "".join(c for c in input_data if c not in punc)
        words_raw = s.strip().split(" ")
        print(words_raw)
        # 3. call model predict function
        preds = learn.predict(words_raw)[0]
        print(preds)
        # 4. process the output
        output_data = align_data({"input": words_raw, "output": preds})
        print(output_data)
        # 5. return the output for the api
        return output_data

    return model_api
