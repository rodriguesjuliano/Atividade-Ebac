import dash
from dash import html,dcc
from dash.dependencies import Input,Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

app=dash.Dash(__name__)

app.layout=html.Div(children=[

])

#=====================INGESTÃO DE DADOS======================
df=pd.read_csv("supermarket_sales.csv")
df['Date']=pd.to_datetime(df['Date'])

#======================= LAYOUTS ==========================
app.layout=html.Div(children=[
    html.H1("Painel de Vendas Supermercado"), #título
    html.Hr(),
    html.H5("Cidades:"),
    dcc.Checklist(id='check_city',
                  options=df['City'].unique(),inline=True,value=df["City"].value_counts().index),#opções de cidade marcaçã opadrão de todas
                   html.H5("Variável de Análise:"),
                    dcc.RadioItems(['gross income','Rating'],value='gross income',id='main_variable',inline=True), #opções de variáveis passando seleção padrão
                    dcc.Graph(id='city_fig'), #gráfico por cidade
                    dcc.Graph(id='pay_fig'), #gráfico por tipo de pagamento
                    dcc.Graph(id='icome_per_product_fig')


])

#======================= CALLBACKS ==========================
@app.callback([
    Output('city_fig','figure'), #figura que eu quero alterar
    Output('pay_fig','figure'),#figura que eu quero alterar
    Output('icome_per_product_fig','figure'),#figura que eu quero alterar
          ],     
              [Input('check_city','value'),
               Input('main_variable','value')]) #ligando checklist com os gráficos

def rander_graphs(cities,main_variable):
    operation=np.sum if main_variable =="gross income" else np.mean
    df_filtered=df[df["City"].isin(cities)] #filtrar as cidades que estiverem no checklist
    #definindo dataframe
    df_city=df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_payment=df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_product_icome=df_filtered.groupby(["Product line","City"])[main_variable].apply(operation).to_frame().reset_index()


    fig_city=px.bar(df_city,x="City",y=main_variable,text_auto='2s',color='City',pattern_shape='City',pattern_shape_sequence=[".", "x", "+"])
    fig_city.update_traces(textposition ="outside")
    fig_payment=px.bar(df_payment,y="Payment",x=main_variable,orientation='h')
    fig_product_icome=px.bar(df_product_icome,x=main_variable,y='Product line',color='City',orientation='h',barmode='group')

    fig_city.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=350)
    fig_payment.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=350)
    fig_product_icome.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=500)
    return fig_city,fig_payment,fig_product_icome
#====================== RUN SERVER ===========================
if __name__=="__main__":
    app.run_server(port=8052,debug=True)