from django import forms
from django.utils.translation import gettext_lazy as _


SCAT_CHOICES1 = [
    ('1', _('Rarely')),
    ('2', _('Sometimes')),
    ('3', _('Often')),
]

SCAT_CHOICES2 = [
    ('0', _('Rarely')),
    ('0', _('Sometimes')),
    ('0', _('Often')),
]


SCAT_CHOICES3 = [
    ('3', _('Rarely')),
    ('2', _('Sometimes')),
    ('1', _('Often')),
]


class SCATForm(forms.Form):
    q1 = forms.ChoiceField(choices=SCAT_CHOICES2, widget=forms.RadioSelect, label=_("Competing against others is socially enjoyable."))
    q2 = forms.ChoiceField(choices=SCAT_CHOICES1, widget=forms.RadioSelect, label=_("Before I compete, I feel uneasy."))
    q3 = forms.ChoiceField(choices=SCAT_CHOICES1, widget=forms.RadioSelect, label=_("Before I compete, I worry about not performing well."))
    q4 = forms.ChoiceField(choices=SCAT_CHOICES2, widget=forms.RadioSelect, label=_("I am a good sportsperson when I compete."))
    q5 = forms.ChoiceField(choices=SCAT_CHOICES1, widget=forms.RadioSelect, label=_("When I compete, I worry about making mistakes."))
    q6 = forms.ChoiceField(choices=SCAT_CHOICES3, widget=forms.RadioSelect, label=_("Before I compete, I am calm."))
    q7 = forms.ChoiceField(choices=SCAT_CHOICES2, widget=forms.RadioSelect, label=_("Setting a goal is important when competing."))
    q8 = forms.ChoiceField(choices=SCAT_CHOICES1, widget=forms.RadioSelect, label=_("Before I compete, I get a queasy feeling in my stomach."))
    q9 = forms.ChoiceField(choices=SCAT_CHOICES1, widget=forms.RadioSelect, label=_("Just before competing, I notice my heart beats faster than usual."))
    q10 = forms.ChoiceField(choices=SCAT_CHOICES2, widget=forms.RadioSelect, label=_("I like to compete in games that demand a lot of physical energy."))
    q11 = forms.ChoiceField(choices=SCAT_CHOICES3, widget=forms.RadioSelect, label=_("Before I compete, I feel relaxed."))
    q12 = forms.ChoiceField(choices=SCAT_CHOICES1, widget=forms.RadioSelect, label=_("Before I compete, I am nervous."))
    q13 = forms.ChoiceField(choices=SCAT_CHOICES2, widget=forms.RadioSelect, label=_("Team sports are more exciting than individual sports."))
    q14 = forms.ChoiceField(choices=SCAT_CHOICES1, widget=forms.RadioSelect, label=_("I get nervous waiting to start the game."))
    q15 = forms.ChoiceField(choices=SCAT_CHOICES1, widget=forms.RadioSelect, label=_("Before I compete, I usually get uptight."))

    notes = forms.CharField(label="Notes (optional)", required=False, widget=forms.Textarea)


CSAI2_CHOICES = [
    ('1', _('Not at all')),
    ('2', _('Somewhat')),
    ('3', _('Moderately so')),
    ('4', _('Very much so')),
]


class CSAI2Form(forms.Form):
    q1 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I am concerned about this competition."))
    q2 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel nervous."))
    q3 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel at ease."))
    q4 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I have self-doubts."))
    q5 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel jittery."))
    q6 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel comfortable."))
    q7 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I am concerned I may not do as well in this competition as I could."))
    q8 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("My body feels tense."))
    q9 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel self-confident."))
    q10 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I am concerned about losing."))
    q11 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel tense in my stomach."))
    q12 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel secure."))
    q13 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I am concerned about losing."))
    q14 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("My body feels relaxed."))
    q15 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I'm confident I can meet the challenge."))
    q16 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I'm concerned about performing poorly."))
    q17 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("My heart is racing."))
    q18 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I'm confident about performing well."))
    q19 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I'm worried about reaching my goal."))
    q20 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel my stomach sinking."))
    q21 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I feel mentally relaxed."))
    q22 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I'm concerned that others will be disappointed with my performance."))
    q23 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("My hands are clammy."))
    q24 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I'm confident because I mentally picture myself reaching my goal."))
    q25 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I'm concerned I won't be able to concentrate."))
    q26 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("My body feels tight."))
    q27 = forms.ChoiceField(choices=CSAI2_CHOICES, widget=forms.RadioSelect, label=_("I'm confident of coming through under pressure."))

    notes = forms.CharField(label="Notes (optional)", required=False, widget=forms.Textarea)


CHOICES = [
    (0, _('Not at all')),
    (1, _('A little')),
    (2, _('Moderately')),
    (3, _('Quite a bit')),
    (4, _('Extremely')),
]


class POMSForm(forms.Form):
    tense = forms.ChoiceField(label=_("Tense: Feeling nervous, anxious, or worried"), choices=CHOICES, widget=forms.RadioSelect)
    angry = forms.ChoiceField(label=_("Angry: Feeling angry or furious"), choices=CHOICES, widget=forms.RadioSelect)
    fatigued = forms.ChoiceField(label=_("Fatigued: Feeling tired or worn out"), choices=CHOICES, widget=forms.RadioSelect)
    depressed = forms.ChoiceField(label=_("Depressed: Feeling sad or hopeless"), choices=CHOICES, widget=forms.RadioSelect)
    vigorous = forms.ChoiceField(label=_("Vigorous: Feeling active and energetic"), choices=CHOICES, widget=forms.RadioSelect)
    confused = forms.ChoiceField(label=_("Confused: Feeling mixed up or unclear headed"), choices=CHOICES, widget=forms.RadioSelect)
    friendly = forms.ChoiceField(label=_("Friendly: Feeling kind and sympathetic"), choices=CHOICES, widget=forms.RadioSelect)
    calm = forms.ChoiceField(label=_("Calm: Feeling peaceful or relaxed"), choices=CHOICES, widget=forms.RadioSelect)
    energetic = forms.ChoiceField(label=_("Energetic: Feeling lively and energetic"), choices=CHOICES, widget=forms.RadioSelect)
    anxious = forms.ChoiceField(label=_("Anxious: Feeling uneasy or apprehensive"), choices=CHOICES, widget=forms.RadioSelect)
    unhappy = forms.ChoiceField(label=_("Unhappy: Feeling sad or unhappy"), choices=CHOICES, widget=forms.RadioSelect)
    sleepy = forms.ChoiceField(label=_("Sleepy: Feeling tired or drowsy"), choices=CHOICES, widget=forms.RadioSelect)
    restless = forms.ChoiceField(label=_("Restless: Feeling fidgety or unable to relax"), choices=CHOICES, widget=forms.RadioSelect)
    cheerful = forms.ChoiceField(label=_("Cheerful: Feeling happy or joyful"), choices=CHOICES, widget=forms.RadioSelect)
    gloomy = forms.ChoiceField(label=_("Gloomy: Feeling sad or down"), choices=CHOICES, widget=forms.RadioSelect)
    energetic_2 = forms.ChoiceField(label=_("Energetic (2): Feeling full of pep"), choices=CHOICES, widget=forms.RadioSelect)
    lonely = forms.ChoiceField(label=_("Lonely: Feeling isolated or alone"), choices=CHOICES, widget=forms.RadioSelect)
    impatient = forms.ChoiceField(label=_("Impatient: Feeling restless or irritated"), choices=CHOICES, widget=forms.RadioSelect)
    cheerful_2 = forms.ChoiceField(label=_("Cheerful (2): Feeling happy"), choices=CHOICES, widget=forms.RadioSelect)
    weak = forms.ChoiceField(label=_("Weak: Feeling physically weak or feeble"), choices=CHOICES, widget=forms.RadioSelect)
    lively = forms.ChoiceField(label=_("Lively: Feeling spirited or full of life"), choices=CHOICES, widget=forms.RadioSelect)
    nervous = forms.ChoiceField(label=_("Nervous: Feeling jittery or tense"), choices=CHOICES, widget=forms.RadioSelect)
    discouraged = forms.ChoiceField(label=_("Discouraged: Feeling downhearted or sad"), choices=CHOICES, widget=forms.RadioSelect)
    confused_2 = forms.ChoiceField(label=_("Confused (2): Feeling mixed up"), choices=CHOICES, widget=forms.RadioSelect)

    notes = forms.CharField(label="Notes (optional)", required=False, widget=forms.Textarea)


class TEOSQForm(forms.Form):
    q1 = forms.IntegerField(label="1) I am the only one who can do the play or skill.", min_value=1, max_value=5)
    q2 = forms.IntegerField(label="2) I learn a new skill, and it makes me want to practice more.", min_value=1, max_value=5)
    q3 = forms.IntegerField(label="3) I can do better than my friends.", min_value=1, max_value=5)
    q4 = forms.IntegerField(label="4) The others cannot do as well as me.", min_value=1, max_value=5)
    q5 = forms.IntegerField(label="5) I learn something fun to do.", min_value=1, max_value=5)
    q6 = forms.IntegerField(label="6) Others mess up, but I do not.", min_value=1, max_value=5)
    q7 = forms.IntegerField(label="7) I learn a new skill by trying hard.", min_value=1, max_value=5)
    q8 = forms.IntegerField(label="8) I work hard.", min_value=1, max_value=5)
    q9 = forms.IntegerField(label="9) I score the most points/goals/hits, etc.", min_value=1, max_value=5)
    q10 = forms.IntegerField(label="10) Something I learn makes me want to practice more.", min_value=1, max_value=5)
    q11 = forms.IntegerField(label="11) I am the best.", min_value=1, max_value=5)
    q12 = forms.IntegerField(label="12) A skill I learn feels right.", min_value=1, max_value=5)
    q13 = forms.IntegerField(label="13) I do my very best.", min_value=1, max_value=5)

    notes = forms.CharField(label="Notes (optional)", required=False, widget=forms.Textarea)
