"""
Main file for the bot.
Author: AlexTraveylan
Date: 27/11/2023
"""
from interactions import (
    Button,
    ButtonStyle,
    Client,
    Embed,
    Intents,
    ModalContext,
    OptionType,
    listen,
    slash_command,
    SlashContext,
    Modal,
    ParagraphText,
    ShortText,
    slash_option,
)
from interactions.api.events import Component
from app.core.constants import DISCORD_BOT_TOKEN
from app.core.ram_memory import RAMemory
from app.core.sondage import Proposition, Question, Sondage

bot = Client(intents=Intents.DEFAULT)


@listen()
async def on_ready():
    """Called when the bot is ready."""
    print("Ready")


@slash_command(name="creer_sondage", description="Commande de test 2")
@slash_option(
    name="nom_sondage",
    description="Le nom du sondage",
    required=True,
    opt_type=OptionType.STRING,
    max_length=20,
)
@slash_option(
    name="nb_propositions",
    description="Le nombre de propositions par question",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=2,
    max_value=4,
)
async def creer_sondage(ctx: SlashContext, nom_sondage: str, nb_propositions: int):
    """Créer un sondage avec un nombre de questions donné."""

    question_modal = Modal(
        ParagraphText(label="Question du sondage", custom_id="question"),
        title="Creation d'un sondage",
    )
    for i in range(nb_propositions):
        short_text = ShortText(
            label=f"Proposition {i+1}", custom_id=f"proposition_{i+1}", max_length=20
        )
        question_modal.add_components(short_text)

    await ctx.send_modal(modal=question_modal)

    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(question_modal)

    question = modal_ctx.responses["question"]
    propositions = [
        modal_ctx.responses[f"proposition_{i+1}"] for i in range(nb_propositions)
    ]

    object_propositions = [Proposition(proposition) for proposition in propositions]
    object_question = Question(question, object_propositions)
    object_sondage = Sondage(nom_sondage, ctx.author.display_name, object_question)

    RAMemory.add_sondage(object_sondage)

    buttons = [
        Button(
            label=f"Choix {i+1}",
            custom_id=f"repondre||{i+1}||{object_sondage.name}",
            style=ButtonStyle.PRIMARY,
        )
        for i in range(nb_propositions)
    ]

    embed = Embed(title=nom_sondage, description=question)
    for i, proposition in enumerate(propositions):
        embed.add_field(name=f"Choix {i+1}", value=proposition)

    await modal_ctx.send(embed=embed, components=buttons)


@listen(Component)
async def on_component(event: Component):
    """Called when a component is clicked."""
    ctx = event.ctx

    if ctx.custom_id.startswith("repondre||"):
        sondage_name = ctx.custom_id.split("||")[2]
        sondage_choice = int(ctx.custom_id.split("||")[1])
        sondage = RAMemory.get_sondage_by_name(sondage_name)
        author_name = event.ctx.author.display_name

        sondage.question.propositions[sondage_choice - 1].author_vote.append(
            author_name
        )

        embed = Embed(
            title=f"Réponse au sondage {sondage_name}",
            description=f"{author_name} a choisi {sondage_choice} au sondage",
        )
        await event.ctx.send(embed=embed)


@slash_command(name="afficher_sondages", description="Afficher les sondages crées")
async def afficher_sondages(ctx: SlashContext):
    """Afficher les sondages crées."""

    sondages_id = RAMemory.get_sondages()

    embed = Embed(title="Sondages crées", description="Liste des sondages crées")

    for index, sondage_id in enumerate(sondages_id):
        embed.add_field(name=f"Sondage n°{index}", value=sondage_id)

    await ctx.send(embed=embed)


bot.start(DISCORD_BOT_TOKEN)
