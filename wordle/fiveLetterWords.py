"""
I'm expecting this to replace fiveLetterWords.txt, which is no more than a list of five-letter words separated by spaces.
I expect each word to have:
  - the word
  - its part of speech
  - its definition
  - any examples
  x possibly its usage
  - its frequency rank
  - (part of) its usefulness score
  - possibly its rank
For now, we are looking at the format being something like this:

{
  'word': {
    'description': 'trailing string (part of speech, def, example)',
    'googleScore': 1,
    'wikiScore': 1,
    'emlimScore': 0,
    'finalScore': 0
  }
}
"""

words = {
    'aahed': {
        'description': '\x1b[1m\x1b[2maahed:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'aalii': {
        'description': '\x1b[1m\x1b[2maalii:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'aargh': {
        'description': '\x1b[1maargh:\x1b[22m interjection. Expressing annoyance, dismay, embarrassment or frustration. \x1b[3m"Argh! Itʼs already 7:15! Weʼre never gonna make it!"\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'aarti': {
        'description': '\x1b[1m\x1b[2maarti:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abaca': {
        'description': '\x1b[1mabaca:\x1b[22m noun. Musa textilis, a species of banana tree native to the Philippines grown for its textile, rope- and papermaking fibre.',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abaci': {
        'description': '\x1b[1m\x1b[2mabaci:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'aback': {
        'description': '\x1b[1maback:\x1b[22m adverb. Towards the back or rear; backwards.',
        'googleScore': 0,
        'wikiScore': 0.0007447125409591897,
    },
    'abacs': {
        'description': '\x1b[1m\x1b[2mabacs:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abaft': {
        'description': '\x1b[1mabaft:\x1b[22m adverb. On the aft side; in the stern. \x1b[3m"The mate sleeps abaft."\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.0002680993898057888,
    },
    'abaka': {
        'description': '\x1b[1m\x1b[2mabaka:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abamp': {
        'description': '\x1b[1m\x1b[2mabamp:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'aband': {
        'description': '\x1b[1m\x1b[2maband:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abase': {
        'description': '\x1b[1mabase:\x1b[22m verb. To lower, as in condition in life, office, rank, etc., so as to cause pain or hurt feelings; to degrade, to depress, to humble, to humiliate.',
        'googleScore': 0,
        'wikiScore': 0.0002509662199467952,
    },
    'abash': {
        'description': '\x1b[1mabash:\x1b[22m verb. To make ashamed; to embarrass; to destroy the self-possession of, as by exciting suddenly a consciousness of guilt, mistake, or inferiority; to disconcert; to discomfit.',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abask': {
        'description': '\x1b[1m\x1b[2mabask:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abate': {
        'description': '\x1b[1mabate:\x1b[22m noun. Abatement.',
        'googleScore': 0,
        'wikiScore': 0.0007835394041966371,
    },
    'abaya': {
        'description': '\x1b[1mabaya:\x1b[22m noun. A coarse, often striped, felted fabric from the Middle East, woven from goat or camel hair.',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abbas': {
        'description': '\x1b[1m\x1b[2mabbas:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.00035783808542310774,
    },
    'abbed': {
        'description': '\x1b[1m\x1b[2mabbed:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abbes': {
        'description': '\x1b[1mabbes:\x1b[22m noun. A French abbot, the (male) head of an abbey.',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abbey': {
        'description': '\x1b[1mabbey:\x1b[22m noun. The office or dominion of an abbot or abbess.',
        'googleScore': 0.002378191979547549,
        'wikiScore': 0.0018743439796071375,
    },
    'abbot': {
        'description': '\x1b[1mabbot:\x1b[22m noun. The superior or head of an abbey or monastery. \x1b[3m"The newly appointed abbot decided to take a tour of the abbey with the cardinal\'s emissary."\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.001318565400843882,
    },
    'abcee': {
        'description': '\x1b[1m\x1b[2mabcee:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abeam': {
        'description': '\x1b[1mabeam:\x1b[22m adjective. Alongside or abreast; opposite the center of the side of the ship or aircraft. \x1b[3m"The island was directly abeam of us."\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abear': {
        'description': '\x1b[1m\x1b[2mabear:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abele': {
        'description': '\x1b[1mabele:\x1b[22m noun. The white poplar (Populus alba).',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abets': {
        'description': '\x1b[1mabets:\x1b[22m noun. Fraud or cunning.',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abhor': {
        'description': '\x1b[1mabhor:\x1b[22m verb. To regard with horror or detestation; to shrink back with shuddering from; to feel excessive repugnance toward; to detest to extremity; to loathe. \x1b[3m"I absolutely abhor being stuck in traffic jams"\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.0007219069895034723,
    },
    'abide': {
        'description': '\x1b[1mabide:\x1b[22m verb. To endure without yielding; to withstand; await defiantly; to encounter; to persevere. \x1b[3m"The old oak tree abides the wind endlessly."\x1b[0m',
        'googleScore': 0.0022029464408646563,
        'wikiScore': 0.003531821713639895,
    },
    'abies': {
        'description': '\x1b[1m\x1b[2mabies:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.00017222256666735554,
    },
    'abled': {
        'description': '\x1b[1mabled:\x1b[22m adjective. (in combination) Having a range of physical powers as specified.',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abler': {
        'description': '\x1b[1mabler:\x1b[22m adjective. Easy to use.',
        'googleScore': 0,
        'wikiScore': 0.0003576230938689097,
    },
    'ables': {
        'description': '\x1b[1m\x1b[2mables:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'ablet': {
        'description': '\x1b[1m\x1b[2mablet:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'ablow': {
        'description': '\x1b[1m\x1b[2mablow:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abmho': {
        'description': '\x1b[1m\x1b[2mabmho:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abode': {
        'description': '\x1b[1mabode:\x1b[22m verb. To endure without yielding; to withstand; await defiantly; to encounter; to persevere. \x1b[3m"The old oak tree abides the wind endlessly."\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.0032577534532186605,
    },
    'abohm': {
        'description': '\x1b[1m\x1b[2mabohm:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'aboil': {
        'description': '\x1b[1m\x1b[2maboil:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'aboma': {
        'description': '\x1b[1m\x1b[2maboma:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'aboon': {
        'description': '\x1b[1m\x1b[2maboon:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.0001710752765431845,
    },
    'abord': {
        'description': '\x1b[1m\x1b[2mabord:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.0002160433815110074,
    },
    'abore': {
        'description': '\x1b[1m\x1b[2mabore:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abort': {
        'description': '\x1b[1mabort:\x1b[22m noun. A miscarriage; an untimely birth; an abortion.',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'about': {
        'description': '\x1b[1mabout:\x1b[22m adjective. Moving around; astir. \x1b[3m"After my bout with Guillan-Barre Syndrome, it took me 6 months to be up and about again."\x1b[0m',
        'googleScore': 0.761904761904762,
        'wikiScore': 0.2222222222222222,
    },
    'above': {
        'description': '\x1b[1mabove:\x1b[22m noun. Heaven.',
        'googleScore': 0.04884004884004884,
        'wikiScore': 0.04329004329004329,
    },
    'abram': {
        'description': '\x1b[1m\x1b[2mabram:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0.0005708935626041881,
    },
    'abray': {
        'description': '\x1b[1m\x1b[2mabray:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abrim': {
        'description': '\x1b[1m\x1b[2mabrim:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
    'abrin': {
        'description': '\x1b[1m\x1b[2mabrin:\x1b[22m No Definitions Found\x1b[0m',
        'googleScore': 0,
        'wikiScore': 0,
    },
}
