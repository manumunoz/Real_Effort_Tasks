from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Results(Page):

    def vars_for_template(self):
        participant = self.participant
        return {
            'redemption_code': participant.label or participant.code,
            'Earnings': participant.payoff,
        }


page_sequence = [
    Results
]
