from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv


author = 'Manu Munoz'

doc = """
Real effort task. A player is shown a word and he has to make new words (min length 5) using the letters of the word shown.
"""

class Constants(BaseConstants):
    name_in_url = 'task_words'
    players_per_group = None

    with open('task_words/list.csv') as f:
        questions = list(csv.DictReader(f))  # PERHAPS INCLUDE THE ANSWERS AS A LIST HERE.

    words = dict()
    words[1] = ['baning','baking','kiang','agin','akin','bang','bani','bank','gain','gink','kain','kina','king']
    words[2] = ['compel','clomp','celom','clop','cole','come','comp','cope','expo','lope','mole','mope','plex','poem',
                'pole','pome']
    words[3] = ['ferric','cirri','citer','crier','firer','frier','icier','recit','recti','refit','ricer','rifer',
                'trice','trier','cire','cite','crit','etic','fice','fire','fret','frit','reft','reif','rice','rife',
                'rift','rite','tier','tire','tref']
    words[4] = ['wofully','fellow','foully','woeful','yellow','felly','foley','folly','fully','lowly','welly','woful',
                'fell','flew','fley','floe','flow','flue','foul','fowl','fuel','full','lowe','well','wolf','wyle',
                'yell','yowe','yowl','yule']
    words[5] = ['rhythm','myths','myth']
    words[6] = ['crypt','pricy','pyric','typic','city','crit','pity','pyic','trip']
    words[7] = ['hypnic','chimp','mincy','nymph','pinch','chin','chip','hymn','inch','piny','pyic','pyin']
    words[8] = ['gipsy','sipes','spies','yipes','egis','gies','espy','gips','gyps','pegs','pies','pigs','piss','psis',
                'pyes','segs','seis','sipe','sips','yeps','yipe','yips']
    words[9] = ['hypnic','phylic','hinny','hiply','lynch','pinch','pinny','chin','chip','clip','inch','inly','lich',
                'linn','liny','lych','pily','piny','pyic','pyin']
    words[10] = ['clutch','cultch','culch','cutch','yucch','cult','lych','yuch']
    words[11] = ['qabala','albas','baals','balas','balsa','basal','sabal','aals','abas','alas','alba','albs','baal',
                 'baas','bals','labs','slab']
    words[12] = ['exogen','oxygen','oxeye','xenon','yogee','exon','eyen','eyne','gene','gone','nene','neon','none',
                 'ogee','onyx','oxen']


    # A better way would maybe be to have alle the answers as lists in a dictionary instead of as seperate lists, then we could just reference the item in the dictionary instead of having
    # to make a list of lists.... A matter of taste.

    num_rounds = 300
    num_words = len(words)

    min_answer_length = 1


class Subsession(BaseSubsession):
    word_points = models.FloatField()

    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['questions'] = Constants.questions

        for i in self.get_players():
            for word in Constants.questions:
                i.participant.vars[word['question']] = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    code = models.StringField()


    word_num = models.PositiveIntegerField(initial=0)
    word_id = models.IntegerField()
    word = models.StringField()
    submitted_answer = models.StringField(blank=True)
    # El blank=True es por ahora valido para testing, luego lo quito
    word_points = models.FloatField()
    word_show = models.PositiveIntegerField(initial=1)
    word_increment = models.IntegerField(initial=0)
    total_payoff = models.CurrencyField(initial=0)

    is_correct = models.BooleanField()
    payoff_score = models.IntegerField()

    def current_question(self):
        if 1 < self.round_number <= Constants.num_rounds:
            self.word_show = self.in_round(self.round_number-1).word_show
        return self.session.vars['questions'][self.word_show-1]

    def word_check(self):
        if self.submitted_answer in Constants.words[self.word_show] and \
                self.submitted_answer not in self.participant.vars[Constants.questions[self.word_show]['question']]:
            self.participant.vars[Constants.questions[self.word_show]['question']].append(self.submitted_answer)

            self.is_correct = True
            # self.payoff_score = (len(self.submitted_answer) - 4)
            self.payoff_score = (max(len(self.submitted_answer),4)-3)
        else:
            self.is_correct = False
            # self.payoff_score = -1 * (len(self.submitted_answer) - 4)
            self.payoff_score = -1 * (max(len(self.submitted_answer),4)-3)


        self.payoff += c(self.payoff_score)
        self.total_payoff = c(sum([p.payoff for p in self.in_all_rounds()]))

    # Checks if the given answer is empty or shorter than the min_lenght, in which case returns false
    def validate_answer(self, answer):
        if len(answer) < Constants.min_answer_length or answer == 'None':
            return False
        return True

    def set_payoffs(self):
        self.payoff = self.payoff_score
