"""Vocabulary content bank for spelling practice.

Stage 3 keeps the first bank intentionally small but structured around the
project's target domains so later stages can scale the set without changing
the calling code.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from uuid import uuid4

from ..models import VocabularyPrompt


@dataclass(frozen=True, slots=True)
class VocabularyItem:
    """A vocabulary entry with multiple prompt styles."""

    word: str
    meaning: str
    example: str
    topic: str
    prompt_types: tuple[str, ...]


VOCABULARY_ITEMS: tuple[VocabularyItem, ...] = (
    VocabularyItem(
        word="influence",
        meaning="the power to affect how someone or something develops, behaves, or thinks",
        example="Teachers can influence how students approach learning.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="maintain",
        meaning="to keep something in the same state or continue something",
        example="Students should maintain a steady study routine before the exam.",
        topic="campus_life",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="significant",
        meaning="large enough or important enough to have an effect",
        example="The study found a significant improvement after the new method was used.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="clarify",
        meaning="to make something easier to understand",
        example="The professor asked the student to clarify the main point.",
        topic="email",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="effective",
        meaning="successful in producing the intended result",
        example="A clear outline can be an effective way to organize ideas.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="perspective",
        meaning="a way of thinking about something",
        example="The discussion offered a new perspective on the issue.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word", "root_hint"),
    ),
    VocabularyItem(
        word="responsibility",
        meaning="a duty to take care of something or someone",
        example="Time management is an important responsibility for university students.",
        topic="campus_life",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="contribute",
        meaning="to help cause something to happen",
        example="Regular practice can contribute to stronger writing performance.",
        topic="academic_discussion",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="handrail",
        meaning="a rail fixed to a wall or post for people to hold on to for support",
        example="She held the handrail while walking down the stairs.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="aquarium",
        meaning="a glass container or building where fish and other water animals are kept",
        example="The aquarium had a bright tank full of tropical fish.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="dock",
        meaning="a platform or area where boats are tied, loaded, or unloaded",
        example="The boat stopped beside the dock.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="pavilion",
        meaning="a separate building or covered structure used for a special purpose",
        example="Students met at the pavilion after class.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="bench",
        meaning="a long seat for several people",
        example="They sat on the bench and watched the park.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="serene",
        meaning="calm, peaceful, and untroubled",
        example="The lake looked serene in the morning light.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="litter",
        meaning="waste that has been left lying in an open place",
        example="The park asked visitors not to litter.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="permit",
        meaning="an official document that gives permission to do something",
        example="You need a permit to park here overnight.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="garage",
        meaning="a building or part of a house used for parking vehicles",
        example="The car was moved into the garage before the rain started.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="rear",
        meaning="the back part of something",
        example="The rear entrance was closed after sunset.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="lane",
        meaning="a narrow road or part of a road marked for a particular use",
        example="The bus stayed in the right lane.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="fine",
        meaning="of high quality; satisfactory; very small or thin",
        example="The surface was smooth and fine.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="tow",
        meaning="to pull a vehicle or object along behind another vehicle",
        example="The truck had to tow the broken car.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="deli",
        meaning="a store that sells prepared foods such as sandwiches and salads",
        example="They bought lunch from the deli near campus.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="insulated",
        meaning="protected by material that prevents heat, sound, or electricity from moving through",
        example="The bottle was insulated to keep the drink warm.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="reptile",
        meaning="a cold-blooded animal with scales, such as a snake or lizard",
        example="The exhibit included a reptile from the desert.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="counter",
        meaning="a flat surface for working on or serving from",
        example="The cashier stood behind the counter.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="disinfect",
        meaning="to clean something with a substance that kills germs",
        example="They disinfect the desk after every session.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="cabinet",
        meaning="a piece of furniture with shelves or drawers used for storage",
        example="The dishes were kept in the cabinet above the sink.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="sturdy",
        meaning="strong and not easily damaged or broken",
        example="The chair looked sturdy enough to last for years.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="unattended",
        meaning="without anyone watching, caring for, or paying attention to it",
        example="Do not leave your bag unattended in the hall.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="compensation",
        meaning="money or something else given to make up for loss, injury, or work",
        example="The company offered compensation after the delay.",
        topic="speaking_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="petroleum",
        meaning="oil obtained from beneath the earth and used to make fuel",
        example="Petroleum is used to produce many fuels and chemicals.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="readiness",
        meaning="the state of being fully prepared",
        example="Her readiness helped the team start on time.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="mutual",
        meaning="felt or done by two or more people in the same way",
        example="Mutual respect makes discussion easier.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="plasterer",
        meaning="a worker who applies plaster to walls and ceilings",
        example="The plasterer repaired the damaged wall.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="plaster",
        meaning="a soft material used to cover walls or a medical dressing for a wound",
        example="The repair team used plaster to finish the wall.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="predisposition",
        meaning="a natural tendency to behave or react in a certain way",
        example="Some students have a predisposition toward cautious planning.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="convey",
        meaning="to communicate or transport something",
        example="The chart conveys the main trend clearly.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="tide",
        meaning="the regular rise and fall of sea level",
        example="The tide came in quickly after noon.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="tidal",
        meaning="relating to the rise and fall of the sea",
        example="The map showed the tidal area near the coast.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="decay",
        meaning="to gradually become worse or rot over time",
        example="Old wood can decay in wet conditions.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="vast",
        meaning="extremely large",
        example="The project covered a vast area of land.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="mammoth",
        meaning="extremely large; also a type of prehistoric elephant",
        example="The museum displayed a mammoth skeleton.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="thrive",
        meaning="to grow and develop strongly",
        example="Plants thrive when they receive enough light.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="pave",
        meaning="to cover a road or path with a hard surface",
        example="The workers pave the walkway near the library.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="leash",
        meaning="a strap or cord used to control an animal",
        example="The dog stayed on a leash during the walk.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="appliance",
        meaning="a device or machine used in the home",
        example="The kitchen appliance was easy to clean.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="drawer",
        meaning="a box-shaped part of a piece of furniture that slides out",
        example="He kept the notes in the drawer.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="utensil",
        meaning="a tool or container used for a particular purpose, especially in the kitchen",
        example="The drawer held every utensil they needed.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="tray",
        meaning="a flat object used for carrying or holding things",
        example="She carried the cups on a tray.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="monstrous",
        meaning="very large, ugly, or shocking",
        example="The beast in the story was described as monstrous.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="carving",
        meaning="an object or design made by cutting material such as wood or stone",
        example="The museum displayed a wooden carving.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="collision",
        meaning="a violent hitting together of two objects or ideas",
        example="The collision damaged both cars.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="agrarian",
        meaning="relating to land, farms, or farming",
        example="The region had an agrarian economy.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="whip",
        meaning="a long thin lash or to strike with one",
        example="The wind seemed to whip around the corner.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="laud",
        meaning="to praise highly",
        example="The article lauds the student's research effort.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="consolidate",
        meaning="to make something stronger or more solid",
        example="The team worked to consolidate its progress.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="levy",
        meaning="to impose or collect a tax or fee",
        example="The city may levy a parking fee.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="bureaucratic",
        meaning="relating to a system of administration that has many rules and offices",
        example="The process became slow and bureaucratic.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="corruption",
        meaning="dishonest or illegal behavior, especially by people in power",
        example="The report discussed corruption in the system.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="socioeconomic",
        meaning="relating to social and economic factors",
        example="The study examined socioeconomic differences among students.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="empirical",
        meaning="based on observation or experience rather than theory",
        example="The findings were supported by empirical data.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="imperial",
        meaning="relating to an empire, emperor, or a very formal and grand style",
        example="The museum had an imperial seal on display.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="contemporaneous",
        meaning="existing or happening at the same time",
        example="The two events were contemporaneous.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="peasant",
        meaning="a poor farmer or rustic person",
        example="The text described the life of a peasant family.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="smallholder",
        meaning="a person who owns or farms a small piece of land",
        example="The area was populated by many smallholder farms.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="downturn",
        meaning="a decline in business, economy, or conditions",
        example="The company faced a sudden downturn.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="spatial",
        meaning="relating to space and the position of objects",
        example="The map required strong spatial reasoning.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="disparity",
        meaning="a clear difference, especially an unfair one",
        example="The article highlighted the disparity between groups.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="monetization",
        meaning="the act of making something into money or using it to earn money",
        example="The app's monetization plan was still being discussed.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="landlocked",
        meaning="surrounded by land and not touching the sea",
        example="The country was landlocked and depended on trade routes.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="aggravated",
        meaning="made worse or more severe",
        example="The delay aggravated the problem.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="stratification",
        meaning="the arrangement of something in layers or classes",
        example="The paper discussed social stratification.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="corroborate",
        meaning="to confirm or support with evidence",
        example="The witness statement corroborated the account.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="burden",
        meaning="a heavy load or a difficult responsibility",
        example="The burden of extra work slowed the team down.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="contest",
        meaning="a competition or to challenge something",
        example="The student did not contest the result.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="pragmatism",
        meaning="the quality of dealing with problems in a practical way",
        example="His pragmatism helped the project move forward.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="ecological",
        meaning="relating to ecology or the environment",
        example="The ecological impact of the project was measured carefully.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="ecology",
        meaning="the study of relationships between living things and their environment",
        example="She decided to study ecology at university.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="fungi",
        meaning="plural of fungus; a group that includes mushrooms and molds",
        example="Fungi can be found in damp soil.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="yeast",
        meaning="a type of fungus used in baking and brewing",
        example="Yeast helps bread dough rise.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="trait",
        meaning="a quality or characteristic of a person or thing",
        example="Patience is a useful trait.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="undergo",
        meaning="to experience or go through a process",
        example="The building will undergo repairs this summer.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="conform",
        meaning="to comply with rules or standards",
        example="Students often conform to classroom expectations.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="vastness",
        meaning="the quality of being very large",
        example="The vastness of the desert was striking.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="swiftly",
        meaning="quickly; at a rapid pace",
        example="The group moved swiftly through the hall.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="radiation",
        meaning="energy that travels as waves or particles",
        example="Radiation can be measured with special equipment.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="span",
        meaning="to stretch across; a period of time; a distance between points",
        example="The bridge spans the river.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="stem",
        meaning="the main part of a plant or the source of something",
        example="Many problems stem from poor planning.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word", "cloze"),
    ),
    VocabularyItem(
        word="vapor",
        meaning="a gas or mist formed by evaporation; vapor is the American spelling of vapour",
        example="Vapor rose from the warm water.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="vapour",
        meaning="a gas or mist formed by evaporation; vapour is the British spelling of vapor",
        example="Vapour filled the room after the shower.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="combat",
        meaning="fighting or to fight against something",
        example="The new plan helps combat waste.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="tangible",
        meaning="real, definite, or able to be touched",
        example="The team made tangible progress.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="intangible",
        meaning="not able to be touched or clearly defined",
        example="Trust is an intangible but important asset.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="resilience",
        meaning="the ability to recover quickly from difficulty",
        example="Resilience helps students adapt to change.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="possess",
        meaning="to have or own something",
        example="Good writers possess strong self-editing habits.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="diversify",
        meaning="to make something more varied or to expand into different areas",
        example="The company decided to diversify its revenue streams.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="strategic",
        meaning="carefully planned to achieve a purpose or connected to strategy",
        example="The team made a strategic decision.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="hierarchical",
        meaning="arranged in levels or ranks",
        example="The organization had a hierarchical structure.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="preconceive",
        meaning="to form an idea before having enough information",
        example="Do not preconceive the result before reading the evidence.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="ornate",
        meaning="elaborately decorated or highly detailed",
        example="The ornate ceiling attracted attention.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="resonate",
        meaning="to produce a strong effect or to echo clearly",
        example="The message seemed to resonate with the audience.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="typeface",
        meaning="a particular design of printed letters",
        example="The article used a simple typeface.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="anthropology",
        meaning="the study of human societies and cultures",
        example="Anthropology examines how people live across cultures.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="prominently",
        meaning="in a way that is easily seen or noticed",
        example="The key idea was displayed prominently on the page.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="interconnected",
        meaning="linked closely together",
        example="The city's systems were highly interconnected.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="inferior",
        meaning="of lower quality or rank",
        example="The older version was clearly inferior.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
    VocabularyItem(
        word="movement",
        meaning="the act of moving or a group organized around a common idea",
        example="The movement gained support quickly.",
        topic="reading_notes",
        prompt_types=("meaning_to_word", "definition_to_word"),
    ),
)


class VocabularyPromptGenerator:
    """Generate vocabulary spelling questions with controlled variation."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = Random(seed)

    def generate(
        self,
        preferred_topic: str = "",
        preferred_prompt_type: str = "",
        preferred_word: str = "",
    ) -> VocabularyPrompt:
        """Return a question that matches one of the supported prompt styles."""

        if preferred_word:
            eligible_items = [item for item in VOCABULARY_ITEMS if item.word == preferred_word]
        else:
            eligible_items = [
                item
                for item in VOCABULARY_ITEMS
                if (not preferred_topic or item.topic == preferred_topic)
                and (not preferred_prompt_type or preferred_prompt_type in item.prompt_types)
            ]
        if not eligible_items:
            eligible_items = list(VOCABULARY_ITEMS)
        item = self._rng.choice(eligible_items)
        prompt_type_pool = list(item.prompt_types)
        if preferred_prompt_type and preferred_prompt_type in prompt_type_pool:
            prompt_type = preferred_prompt_type
        else:
            prompt_type = self._rng.choice(prompt_type_pool)
        prefix_hint = self._build_prefix_hint(item.word)
        prompt_text = self._build_prompt_text(item, prompt_type)
        return VocabularyPrompt(
            prompt_id=str(uuid4()),
            prompt_type=prompt_type,
            topic=item.topic,
            prompt_text=prompt_text,
            prefix_hint=prefix_hint,
            answer=item.word,
            meaning=item.meaning,
            example=item.example,
        )

    def _build_prompt_text(self, item: VocabularyItem, prompt_type: str) -> str:
        if prompt_type == "meaning_to_word":
            return f"Spell the TOEFL vocabulary word for this meaning: {item.meaning}"
        if prompt_type == "definition_to_word":
            return f"Write the word that matches this definition: {item.meaning}"
        if prompt_type == "cloze":
            return f"Complete the sentence: {self._build_cloze(item.example, item.word)}"
        if prompt_type == "root_hint":
            return f"Spell the word using this hint: related to 'view' or 'look' in a broader sense."
        return f"Spell this word: {item.word}"

    @staticmethod
    def _build_cloze(example: str, answer: str) -> str:
        lower_example = example
        return lower_example.replace(answer, "_____", 1)

    @staticmethod
    def _build_prefix_hint(word: str) -> str:
        """Return a short opening fragment that still leaves room to recall the full word."""

        if len(word) <= 6:
            prefix_length = 1
        elif len(word) <= 9:
            prefix_length = 2
        else:
            prefix_length = 3
        return word[:prefix_length]
