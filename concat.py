import streamlit as st
import numpy as np
import pandas as pd
import openpyxl
from openpyxl import Workbook
from io import BytesIO

st.title('🗃️ Juntando diferentes bases em uma base única')
st.caption('Feito com 🧠 por [Blue AI](https://blueai.com.br/)')
st.info('Este app torna fácil juntar múltiplas bases em uma só, através da função concatenar. **Os arquivos aqui carregados não são salvos, copiados ou armezados pela Blue AI** em nenhum momento. Esta aplicação é gratuita, **você pode usar quando e o quanto quiser**. O código desta aplicação em breve estará aberto e será público.')

st.markdown('\n\n')
st.write('##### 1) Comece escolhendo os seus arquivos')
col1, col2 = st.columns([1.5, 2.5])

with col1:
    file_type = st.radio(
        "1.1) Selecione o tipo dos arquivos: 👉",
        options=["CSV (.csv)", "Excel (.xlsx)", "Excel (.xls)"],
    )

with col2:
    if file_type == "CSV (.csv)":
        input_dataframe = st.file_uploader(label = "1.2) Carregue as suas bases aqui, quantas for necessário: 👇", type = 'csv', accept_multiple_files=True)
    elif file_type == "Excel (.xlsx)":
        input_dataframe = st.file_uploader(label = "1.2) Carregue as suas bases aqui, quantas for necessário: 👇", type = 'xlsx', accept_multiple_files=True)
    elif file_type == "Excel (.xls)":
        input_dataframe = st.file_uploader(label = "1.2) Carregue as suas bases aqui, quantas for necessário: 👇", type = 'xls', accept_multiple_files=True)
    else:
        pass

if file_type == "CSV (.csv)":
    if input_dataframe:
        df_list = {}
        file_list = []
        column_list = []

        df_concat_list = {}

        for i in range(len(input_dataframe)):
            df_list[input_dataframe[i].name] = pd.read_csv(input_dataframe[i])
            file_list.append(input_dataframe[i].name)
            column_list.append(df_list[input_dataframe[i].name].columns)

        selected_columns = st.multiselect('Selecione as colunas desejadas, a partir do primeiro arquivo:', column_list[0])

        for i in range(len(input_dataframe)):
            try:
                st.success('**' + input_dataframe[i].name + ':**' + len(df_list[input_dataframe[i].name][selected_columns]) + ' linhas', icon="✅")
                df_concat_list[input_dataframe[i].name] = df_list[input_dataframe[i].name][selected_columns]
                df_list[input_dataframe[i].name][selected_columns]
                st.write(len(df_list[input_dataframe[i].name][selected_columns]))
            except KeyError:
                st.error('**' + input_dataframe[i].name + ':** Verifique se as colunas selecionadas fazem parte deste arquivo', icon="🚨")

        try:
            # st.write(df_concat_list.values())
            df_concat = pd.concat(df_concat_list.values(), ignore_index=True)
            df_concat[selected_columns]
            st.write(len(df_concat))
            def to_excel(df):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df_concat[selected_columns].to_excel(writer, index=False, sheet_name='Sheet1')
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                format1 = workbook.add_format({'num_format': '0.00'}) 
                worksheet.set_column('A:A', None, format1)  
                writer.close()
                processed_data = output.getvalue()
                return processed_data
            df_xlsx = to_excel(df_concat[selected_columns])
            st.download_button(label='📥 Baixar Planilha',
                                            data=df_xlsx ,
                                            file_name= 'arquivos_compilados.xlsx')
        except ValueError:
            st.error('Verifique se os campos acima foram preenchidos corretamente', icon="🚨")
else:
    if input_dataframe:
        df_list = {}
        file_list = []
        column_list = []

        df_concat_list = {}

        for i in range(len(input_dataframe)):
            df_list[input_dataframe[i].name] = pd.read_excel(input_dataframe[i])
            file_list.append(input_dataframe[i].name)
            column_list.append(df_list[input_dataframe[i].name].columns)

        st.markdown('\n\n')
        st.markdown('##### 2) Selecione as colunas desejadas, a partir do primeiro arquivo')
        selected_columns = st.multiselect('Escolha as colunas que devem ser usadas ao compilar os arquivos, tendo o primeiro arquivo da lista como referência:', column_list[0])

        for i in range(len(input_dataframe)):
            try:
                # st.success(input_dataframe[i].name, icon="✅")
                st.success(input_dataframe[i].name + ': **' + str(len(df_list[input_dataframe[i].name][selected_columns])) + ' linhas**', icon="✅")
                df_concat_list[input_dataframe[i].name] = df_list[input_dataframe[i].name][selected_columns]
                df_list[input_dataframe[i].name][selected_columns]
                # st.write(len(df_list[input_dataframe[i].name][selected_columns]))
            except KeyError:
                st.error('**' + input_dataframe[i].name + ':** Arquivo não considerado, verifique se as colunas selecionadas fazem parte deste arquivo', icon="🚨")

        try:
            # st.write(df_concat_list.values())
            st.markdown('\n\n')
            st.markdown('##### 3) Avalie o resultado e baixe o seu arquivo')
            df_concat = pd.concat(df_concat_list.values(), ignore_index=True)
            st.info('Arquivo compilado: **' + str(len(df_concat)) + ' linhas**', icon="ℹ️")
            df_concat = pd.concat(df_concat_list.values(), ignore_index=True)
            df_concat[selected_columns]
            # st.write(len(df_concat))

            def to_excel(df):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df_concat[selected_columns].to_excel(writer, index=False, sheet_name='Sheet1')
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                format1 = workbook.add_format({'num_format': '0.00'}) 
                worksheet.set_column('A:A', None, format1)  
                writer.close()
                processed_data = output.getvalue()
                return processed_data
            df_xlsx = to_excel(df_concat[selected_columns])
            st.download_button(label='📥 Baixar Planilha',
                                            data=df_xlsx ,
                                            file_name= 'arquivos_compilados.xlsx')
        except ValueError:
            st.error('Verifique se os campos acima foram preenchidos corretamente', icon="🚨")
