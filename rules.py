rules = {
    'START': [
        'END',
        'BLOCK_START',
        'STRING',
    ],
    'BLOCK_START': [
        'BLOCK_START',
        'BLOCK_END',
        'STRING',
    ],
    'BLOCK_END': [
        'END',
        'BLOCK_END',
        'KEYWORD',
    ],
    'STRING': [
        'END',
        'BLOCK_END',
        'KEYWORD',
    ],
    'KEYWORD': [
        'BLOCK_START',
        'STRING',
    ]
}

keywords = ["AND", "OR"]

keywords_priority = dict([keyword[::-1] for keyword in list(enumerate(keywords))])
