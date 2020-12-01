##################################################################################
#  You can add your actions in this file or create any other file in this folder #
##################################################################################

from rasa_sdk import Action
from rasa_sdk.events import SlotSet, ReminderScheduled, ConversationPaused, ConversationResumed, FollowupAction, Restarted, ReminderScheduled
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from deep_translator import GoogleTranslator
import json
import random
from typing import Any, Text, Dict, List
import fasttext

import logging
logger = logging.getLogger(__name__)


class ActionMyKB(ActionQueryKnowledgeBase):
    def __init__(self):
        # load knowledge base with data from the given file
        knowledge_base = InMemoryKnowledgeBase("knowledge_base_data.json")

        # overwrite the representation function of the hotel object
        # by default the representation function is just the name of the object
        knowledge_base.set_representation_function_of_object(
            "hotel", lambda obj: obj["name"] + " (" + obj["city"] + ")"
        )

        super().__init__(knowledge_base)


class LanguageIdentification(object):
    def __init__(self):
        pretrained_lang_model = "lid.176.ftz"
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text)  # returns top 2 matching languages
        return predictions[0][0].split('__')[-1]


class MultilingualResponse(object):
    def __init__(self):
        # with open("multilingual_response.json") as fp:
        with open("multilingual_responses.json") as fp:
            self.multilingual_response = json.load(fp)

    @staticmethod
    def random_response(responses):
        num_response = len(responses) - 1
        return responses[random.randint(0, num_response)]

    def predict_response(self, intent, lang):
        default_lang = 'en'
        try:
            mling_response = self.multilingual_response[intent]
            try:
                responses = mling_response[lang]
                final_response = self.random_response(responses)
            except:
                # if language detection fails (ie detects other than languages listed in the response)
                # fallback to English
                responses = mling_response[default_lang]
                final_response = self.random_response(responses)
        except:
            final_response = None
        return final_response


multilingual_response = MultilingualResponse()
language_detection = LanguageIdentification()


class ActionLanguageSelect(Action):

    def name(self) -> Text:
        return "action_utter_language_select"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(tracker.latest_message)
        # print(tracker.events)
        intent = tracker.latest_message['intent'].get('name')
        input_text = tracker.latest_message['text']
        lang = language_detection.predict_lang(input_text)
        response = multilingual_response.predict_response(intent=intent, lang=lang)
        if response:
            logger.info('Multilingual Response:{0}'.format(response))
            dispatcher.utter_message(text=response)
        else:
            utter_intent = "utter_{}".format(intent)
            response_default = domain.get('responses').get(utter_intent)[0].get('text')
            if response_default:
                if lang == 'en':
                    logger.info('Setting default response for the intent:{0}, '
                                'in language:{1}.'.format(intent, lang))
                    dispatcher.utter_message(text=response_default)
                else:
                    logger.info('There is no multilingual response for intent:{0}, '
                                'in language:{1}. Running online translation.'.format(intent, lang))
                    if lang == 'zh':
                        # Change the language from 'zh' to 'zh-cn', as google translate is not supported with zh
                        lang = "{}-cn".format(lang)
                    response_translated = GoogleTranslator(source='en', target=lang).translate(response_default)
                    dispatcher.utter_message(text=response_translated)
        return []
