from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time

class Start(Page):
    form_model = 'player'
    form_fields = ['code']

    def is_displayed(self):
        return self.round_number == 1


    def code_error_message(self, value):
        if len(value) != 10 :
            return 'The code must be 10-digits long'


    def before_next_page(self):
        # user has 5 minutes to complete as many pages as possible
        self.participant.vars['expiry_timestamp'] = time.time() + 5*60

class Sum(Page):
    form_model = 'player'
    form_fields = ['answer']

    def vars_for_template(self):
        self.player.initialize()

        return {
        }

        participant.vars['num_correct'] = self.player.num_correct

    def before_next_page(self):
        if self.player.answer == self.player.solution:
            self.player.answer_correct = 1
        self.player.set_payoff()

        timer_text = 'Time left to complete this task:'

    def get_timeout_seconds(self):
        return self.participant.vars['expiry_timestamp'] - time.time()

    def is_displayed(self):
        return self.participant.vars['expiry_timestamp'] - time.time() > 3


page_sequence = [
    Start,
    Sum,
]
