import gradio as gr
from themeclassification import ThemeClassifier
import pandas as pd 
from characternetwork import CharacterNetwork
from characternetwork import CharacterNetworkGenerator,CharacterNetwork
def get_themes(themelist,subpath,savepath):
    theme_list = themelist.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subpath,savepath)
    df = output_df
    df.drop(['episode','script'],axis=1,inplace=True)
    df = df.sum().reset_index()
    df.columns=['theme','score']
    df.to_csv(savepath)

    # theme_list = [theme for theme in theme_list if theme!='dialogue']
    # output_df = output_df[theme_list]
    # output_df = output_df[theme_list].sum().reset_index()
    # output_df.columns = ['theme','score']
    plot = gr.BarPlot(
        df,
        x='theme',
        y='score',
        title='SeriesThemees',
        vertical=False,
        height = 260,
        width = 500
    )
    return plot


def getnetwork(subpath,nerpath):
    ner = CharacterNetwork()
    nerdf = ner.get_ners(dataset_path=subpath,save_path=nerpath)
    characternetwork = CharacterNetworkGenerator()
    df = characternetwork.charactergenerator(nerdf)
    html = characternetwork.draw_network(df)

    return html




def main():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                gr.HTML('<h1> Classification </h1>')
        with gr.Row():
            with gr.Column():
                plot = gr.BarPlot()

            with gr.Column():  
                themelist = gr.Textbox(label="Themes")      
                subpath = gr.Textbox(label="SubtitlePath")      
                savepath = gr.Textbox(label="SavePath")      
                getthemes = gr.Button("Get Themes")
                getthemes.click(get_themes,inputs=[themelist,subpath,savepath],outputs=[plot])



        with gr.Row():
            with gr.Column():
                gr.HTML('<h1> Character Network </h1>')
        with gr.Row():
            with gr.Column():
                networkplot = gr.HTML()
            with gr.Column():  
                 
                subpath = gr.Textbox(label="SubtitlePath")      
                nerpath = gr.Textbox(label="NERSAVEPATH")      
                get_network = gr.Button("Get NER")
                get_network.click(getnetwork,inputs=[subpath,nerpath],outputs=[networkplot])

                          
    demo.launch()


if __name__ == "__main__":
    main()