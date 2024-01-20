
class Definition():
    def __init__(self):
        self.definition = {
            'word':'',
            'translation':'',
            'tabs':[],    # informs which of "Example","Dictionary","Phrase",or "Conjugations"
                            #    were present on definition page - will add hyperlinks to each
            'subword':[],
            'type':[],
            'details':[
                #* Outline of what should be added
                # {'subdefinitions':[
                #     {'subdefinition':'1. (subdefinition)','subtranslations':[
                #         {'subtranslation':'a. subtranslation','example':'...'}
                #     ]} 
                # ]}
            ]
        }

