DIALOG_DATA = {
    'mary': {
        'default': {
            'dialog': [
                "normal<>dialog<>Good Morning Baby, \nI hope you you're ready for school! I love you so much",
                "sus<>dialog<>Goodbye Baby.",
                "normal<>choices<>Shut up![]cr1()Thanks Mom. I love you so much[]cr2"
            ]
        },
        'slut': {
            'condition': {
              'stats<>lust': '> 50',  
            },
            'dialog': [
                "sus<>dialog<>Hey Baby, My pussy is wet right now",
                "sus<>dialog<>Please a lick with suffice or \n............\nI will ask damien to do it for you."
            ]
        }
    }
}

RESPONSE_DATA = {
    'cr1': {
        'effect': {
            'stats<>love': '- 5'
        },
        'dialog': [
            "sus<>dialog<>I'm Sorry honey for getting in your face"
        ]
    },
    'cr2': {
        'effect': {
            'stats<>love': '+ 5',
            'stats<>lust': '+ 20'
        },
        'dialog': [
            "normal<>dialog<>Thank you so much Baby\nI love you too Baby."
        ]
    }
}