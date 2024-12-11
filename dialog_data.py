

DIALOG_DATA = {
    'mary': {
        'default': {
            'dialog': [
                ["Mary", "normal", "dialog", "Good Morning Baby, \nI hope you you're ready for school! I love you so much"],
                [
                    "MC",
                    "normal", 
                    "choices", 
                    {
                        "Shut up!": {
                            "effect": [["stats", "love", -5], ["stats", "lust", 20], ["buff", "add", "Slut"]],
                            "dialog": [
                                ["MC", "sus", "dialog", "Shut up! Mom, It's your fault we're in this mess."],
                                ["Mary", "sus", "dialog", "I'm sorry baby, I will do better next time."]
                            ]
                        },
                        "Thanks Mom. I love you so much": {
                            "effect": [["stats", "love", 5], ['action', 'decrease', 3]],
                            "dialog": [
                                ["MC", "normal", "dialog", "/I know most of the stuff here is her fault but shit just happens y'know\nshe is not in control of what to happen she just didn't expect it and \nchose the wrong decision."],
                                ["MC", "normal", "dialog", "Thanks Mom, We will get through this. I love you so much"],
                                ["Mary", "normal", "dialog", "Thank you Baby, Have a good day at school"]
                            ]
                        },
                        "Fuck you!": {
                            "effect": [["stats", "love", -5], ["stats", "lust", 20], ["buff", "add", "Slut"]],
                            "dialog": [
                                ["MC", "sus", "dialog", "Shut up! Mom, It's your fault we're in this mess."],
                                ["Mary", "sus", "dialog", "I'm sorry baby, I will do better next time."]
                            ]
                        }
                    }
                ],
                ["Mary", "normal", "dialog", "Good Bye Baby"]
            ]
        },
        'slut': {
            'condition': [["stats", "lust", "> 50"]],
            'dialog': [
                ["Mary", "sus", "dialog", "Hey Baby, My pussy is kinda itchy"],
                ["Mary", "sus", "dialog", "I would like to go to the ghetto, Im just gonna buy something there \n............\nI already baught canned food just microwave it okay? love you."]
            ]
        },
        'incest': {
            'condition': [["buff", "with", "incest"]],
            'dialog': [
                ["Mary", "sus", "dialog", "Hey Baby, My pussy is wet right now"],
                ["Mary", "sus", "dialog", "Please a lick with suffice or \n............\nI will ask damien to do it for you."]
            ]
        }
    }
}