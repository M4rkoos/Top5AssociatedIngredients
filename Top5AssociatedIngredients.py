import requests
import json
import pandas as pd
import time
import seaborn as sns

# http://www.recipepuppy.com/about/api/
# added criteria for page < 25 to avoid too many requests

enter_ingredients_here = ['spinach', 'garlic']
input_len = len(enter_ingredients_here)


def get_recipes(ingredients = enter_ingredients_here, food_type = ''):
    page = 1
    df_final = pd.DataFrame(columns = ['page', 'title', 'version', 'href' , 'results'])
    df_contains_data = True
  
    while df_contains_data and page < 25:        
        parameters = {'i': ingredients, 'q': food_type, 'p': page}
        try:
            response = requests.get("http://www.recipepuppy.com/api/", params = parameters)
            data = response.json()
            data = json.dumps(data['results'])
            df_temp = pd.read_json(data)
            df_temp['page'] = page
            
            if df_temp.empty:
                df_contains_data = False
            else:
                df_final = pd.concat([df_final, df_temp])  
                page += 1
                time.sleep(1)
        except ValueError:
            page +=1
                 
    return df_final

df_output = get_recipes()
df_output_reduced = df_output[['title', 'ingredients']]
df_ingredients = df_output['ingredients'].str.split(', ', expand = True)
df_output_reduced = pd.concat([df_output_reduced['title'], df_ingredients], axis = 1)
df_melt = df_output_reduced.melt(id_vars=['title'], var_name='ingredient_num', value_name='ingredient')
df_grouped = df_melt.groupby('ingredient').count()
df_grouped.rename(columns={'title':'count'}, inplace = True)
df_top_five = df_grouped.sort_values(by=['count'], ascending=False).iloc[input_len: 5 + input_len].reset_index()
sns.barplot(x='ingredient', y='count', data = df_top_five)
