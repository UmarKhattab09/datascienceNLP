from pyvis.network import Network

import networkx as nx
# from charactnetwork import CharacterNetwork

import pandas as pd

class CharacterNetworkGenerator():
    def __init__(self):
        pass

    def charactergenerator(self,df2):
        test =[]
        entityrelationship=[]
        for row in df2['ners']:
            entity = []
            for sentence in row:
                # entity.extend(list(sentence))
                entity.extend(list(sentence))
            test.append(entity)
    #Flatten
            flatten = sum(test,[])
            for sentence in row:
                for entity in sentence:
                    for entitywindow in flatten:
                    # print(entitywindow,entity)
                        if entity!= entitywindow:
                            entityrelationship.append(sorted((entity,entitywindow)))
        relationship_df = pd.DataFrame({"value":entityrelationship})
        relationship_df['source'] = relationship_df['value'].apply(lambda x:x[0])
        relationship_df['target'] = relationship_df['value'].apply(lambda x:x[1])
        relationship_df=relationship_df.groupby(['source','target']).count().reset_index()
        relationship_df=relationship_df.sort_values('value',ascending=False)

        return relationship_df
    

    def draw_network(self,relationship_df):
        relationship_df=relationship_df.head(100)
        
        G = nx.from_pandas_edgelist(
            relationship_df,
            source='source',
            target='target',
            edge_attr='value',
            create_using=nx.Graph()

        )
        net=Network(notebook=True,width="1000px",height="700px",font_color="black",cdn_resources='remote')
        node_degree =dict(G.degree)
        net.from_nx(G)
        # net.show("slayer.html")
        html = net.generate_html()
        html = html.replace("'","\"")


        output_html = f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
    display-capture; encrypted-media;" sandbox="allow-modals allow-forms
    allow-scripts allow-same-origin allow-popups
    allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
    allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""
        
        return output_html


    
# ner = CharacterNetwork()  # ✅ instantiate
# dftest = ner.get_ners(
#     dataset_path="C:/Users/khatt/Documents/DemonSlayer/data/*.ass",
#     save_path="C:/Users/khatt/Documents/DemonSlayer/output/test4.csv"
# )
# test = CharacterNetworkGenerator()
# df = test.charactergenerator(dftest)
# df2 = test.draw_network(df)