from recipe.utils.base.model import BaseModel

import psycopg2
import os

class RequirementValidator(BaseModel):
    def __init__(self):
        super().__init__('Requirement Validator v1')

    @staticmethod
    def validate(recipe_id):
        requirements_needed = []
        ingredients_to_update = []
        with psycopg2.connect(RequirementValidator.get_connection_string()) as conn:
            with conn.cursor() as curs:
                with open(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'requirement_check.sql')) as template:
                    query = template.read()
                    query = query.replace('[RECIPE_ID]', str(recipe_id))

                    curs.execute(query)

                    for requirement in curs:
                        if requirement[-1] < 0:
                            req_info = {}
                            req_info['name'] = requirement[2]
                            req_info['amount_missing'] =  -1 *  requirement[-1]
                            req_info['unit'] = requirement[-3]
                            requirements_needed.append(req_info)
                        else:
                            ingredients_to_update.append((requirement[1], requirement[3]))

        return (requirements_needed, ingredients_to_update)
                    

        
                    