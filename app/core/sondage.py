""" Modèle de données pour les sondages. """


class Proposition:
    """Proposition d'une question d'un sondage."""

    _nb_instances = 0

    def __init__(self, proposition: str):
        self.proposition_id = Proposition._nb_instances
        Proposition._nb_instances += 1
        self.proposition = proposition
        self.author_vote = []


class Question:
    """Question d'un sondage."""

    _nb_instances = 0

    def __init__(self, content: str, propositions: list[Proposition]):
        self.question_id = Question._nb_instances
        Question._nb_instances += 1
        self.content = content
        self.propositions = propositions


class Sondage:
    """Sondage créé par un utilisateur."""

    _nb_instances = 0

    def __init__(self, name: str, author_name: str, question: Question):
        self.name = f"{name}_ID_{Sondage._nb_instances}"
        Sondage._nb_instances += 1
        self.author_name = author_name
        self.question = question
