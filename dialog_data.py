from enums import *

DIALOG_DATA = {
    'mary': {
        'default': {
            'dialog': [
                ["Mary", "normal", "dialog", "Sample Dialog Dialog 1"],
                [
                    "MC",
                    "normal", 
                    "choices", 
                    {
                        "Sample Choice 1": {
                            "effect": [["stats", "love", -5], ["stats", "lust", 20], ["buff-add", "time", CNST_BUFF_MARY_01]],
                            "dialog": [
                                ["MC", "sus", "dialog", "Sample Dialog Dialog 2"],
                                ["Mary", "sus", "dialog", "Sample Dialog Dialog 3"]
                            ]
                        },
                        "Sample Choice 2": {
                            "effect": [['action', 'decrease', 3], ["buff-add", "date", CNST_BUFF_MARY_02]],
                            "dialog": [
                                ["MC", "normal", "dialog", "Sample Dialog Dialog 4"],
                                ["MC", "normal", "dialog", "Sample Dialog Dialog 5"],
                                ["Mary", "normal", "dialog", "Sample Dialog Dialog 6"]
                            ]
                        },
                        "Sample Choice 3": {
                            "effect": [["stats", "love", -5], ["stats", "lust", 20], ["buff-add", "immediate", CNST_BUFF_MARY_03]],
                            "dialog": [
                                ["MC", "sus", "dialog", "Sample Dialog Dialog 7"],
                                ["Mary", "sus", "dialog", "Sample Dialog Dialog 8"]
                            ]
                        }
                    }
                ],
                ["Mary", "normal", "dialog", "Sample Dialog Dialog 9"]
            ]
        },
        'dlg-02': {
            'condition': [["stats", "lust", "> 50"]],
            'dialog': [
                ["Mary", "sus", "dialog", "Sample Dialog Dialog 13"],
                ["Mary", "sus", "dialog", "Sample Dialog Dialog 14"]
            ]
        },
        'dlg-01': {
            'condition': [["buff", "with", "buff01"]],
            'dialog': [
                ["Mary", "sus", "dialog", "Sample Dialog Dialog 11"],
                ["Mary", "sus", "dialog", "Sample Dialog Dialog 12"]
            ]
        }
    }
}