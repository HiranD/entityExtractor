from collections import OrderedDict
from spacy.en import English
import json
import logging
import traceback

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('extractorService.log', 'w', 'UTF-8')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s(%(module)s:%(lineno)d)  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

parser = English()


def sentences(doc):
    parsed_data = parser(doc)
    for span in parsed_data.sents:
        sent = ''.join(parsed_data[i].string for i in range(span.start, span.end)).strip()
        yield sent


def names_ex(sentence):
    parsed_ex= parser(sentence)
    ents = list(parsed_ex.ents)
    dic = OrderedDict()
    for entity in ents:
        dic[' '.join(t.orth_ for t in entity)] = entity.label_

    return dic


def get_names(sent):
    logger.info(sent)
    response = []
    selected_entities = ["PERSON", "NORP", "FACILITY", "ORGANIZATION", "LOCATION",
                         "GPE", "PRODUCT", "EVENT", "WORK_OF_ART", "LANGUAGE"]

    try:
        for sentence in sentences(sent):
            dict = {
                "PERSON": [],
                "NORP": [],
                "FACILITY": [],
                "ORGANIZATION": [],
                "LOCATION": [],
                "GPE": [],
                "PRODUCT": [],
                "EVENT": [],
                "WORK_OF_ART": [],
                "LANGUAGE": [],
                "DATE": [],
                "TIME": [],
                "PERCENT": [],
                "MONEY": [],
                "QUANTITY": [],
                "ORDINAL": [],
                "CARDINAL": [],
            }
            nam = names_ex(sentence)
            for key, value in nam.items():
                if value == "LOC":
                    value = "LOCATION"
                if value == "ORG":
                    value = "ORGANIZATION"
                if value == "FAC":
                    value = "FACILITY"

                if key not in dict[value]:
                    dict[value].append(key)

            ent = {}
            for key, value in dict.items():
                if key in selected_entities:
                    if len(value) != 0:
                        ent[key] = value

            logger.info(ent)
            res = {"sentence": sentence, "entities": ent}
            response.append(res)

    except Exception as e:
        logging.error("error: " + str(e))
    # logging.error(traceback.format_exc())

    # logging.info(response)
    return json.dumps(response)
