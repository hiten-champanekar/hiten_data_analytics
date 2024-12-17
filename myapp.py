#import all libraries 
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
          page_title = "Hiten's Analytics Portal",
          page_icon = "🦁"
)
#title
st.title(":rainbow[Data Analytics Portal]")
#header
st.header("Explore :red[Data] with ease")
st.subheader(":gray[You majesty]",divider='rainbow')
file = st.file_uploader('Drop csv or excel file', type = ['csv', 'xlsx'])
if(file != None): 
          #read uploaded file
          if(file.name.endswith('csv')):
                  data = pd.read_csv(file)
          else:
                  data = pd.read_excel(file)
          
          st.dataframe(data)
          st.info("File is successfully Uploaded", icon = '🚨')
          st.subheader(':rainbow[Basic information of the dataset]',divider='rainbow')
          tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Top and Bottom', 'Data Types', 'Columns'])

          with tab1:
            st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset')
            st.subheader(':gray[Statistical summary of the dataset]')
            st.dataframe(data.describe())
          with tab2:
            st.subheader(':gray[Top Rows]')
            toprows = st.slider('Number of rows you want', 1, data.shape[0],key = 'topslider')
            st.dataframe(data.head(toprows))
            st.subheader(':gray[Bottom Rows]')
            bottomrows = st.slider('Number of rows you want', 1, data.shape[0], key = 'bottomslider')
            st.dataframe(data.head(bottomrows))
          with tab3:
                st.subheader(':gray[Data types of cloumn]')
                st.dataframe(data.dtypes)
          with tab4:
                st.subheader(':gray[Column names in Dataset]')
                st.write(data.columns)

          st.subheader(':rainbow[Column values to count]', divider = 'rainbow')
          with st.expander('Value Count'):
                col1, col2 = st.columns(2)
                with col1:
                        column = st.selectbox('Choose Column name', options=list(data.columns))
                with col2:
                        toprows = st.number_input('Top rows', min_value=1, step=1)
                
                count = st.button('Count')
                if(count==True):
                        result = data[column].value_counts().reset_index().head(toprows)
                        st.dataframe(result)
                        st.subheader('Visualtization', divider='gray')
                        fig = px.bar(data_frame=result, x=column, y='count', text='count', template = 'plotly_white')
                        st.plotly_chart(fig)
                        fig = px.line(data_frame=result,x=column, y = 'count', text='count', template = 'plotly_white')
                        st.plotly_chart(fig)
                        fig = px.pie(data_frame=result, names=column, values='count')
                        st.plotly_chart(fig)
          st.subheader(':rainbow[Groupby : Simplify for your data analysis]', divider='rainbow')
          st.write("The groupby let's you summarize data by specific categories and groups")
          with st.expander('Groupby your columns'):
                col1, col2 , col3 = st.columns(3)
                with col1:
                        groupby_cols = st.multiselect('Choose your column to groupby', options = list(data.columns))
                with col2:
                        operation_col = st.selectbox('Choose column for operation', options = list(data.columns))
                with col3:
                        operation = st.selectbox('Choose operation', options = ['sum', 'max', 'min', 'mean', 'median', 'count'])

                if(groupby_cols):

                        result = data.groupby(groupby_cols).agg(
                                newcol = (operation_col,operation)
                        ).reset_index()

                        st.dataframe(result)

                        st.subheader(':gray[Data Visualization]', divider = 'gray')
                        graphs = st.selectbox('Choose your graphs', options = ['line', 'bar', 'scatter', 'pie', 'sunburst'])
                        if(graphs == 'line'):
                                x_axis = st.selectbox('Choose X axis', options = list(result.columns))
                                y_axis = st.selectbox('Choose Y axis', options = list(result.columns))
                                color = st.selectbox('Color Information', options = [None] + list(result.columns))
                                fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers='o')
                                st.plotly_chart(fig)
                        elif(graphs == 'bar'):
                                x_axis = st.selectbox('Choose X axis', options = list(result.columns), key = 'x_axis')
                                y_axis = st.selectbox('Choose Y axis', options = list(result.columns), key = 'y_axis')
                                color = st.selectbox('Color Information', options = [None] + list(result.columns), key='color')
                                facet_col = st.selectbox('Color Information', options = [None] + list(result.columns), key='facet_col')
                                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                                st.plotly_chart(fig)
                        elif(graphs == 'scatter'):
                                x_axis = st.selectbox('Choose X axis', options = list(result.columns), key = 'x_axis')
                                y_axis = st.selectbox('Choose Y axis', options = list(result.columns), key = 'y_axis')
                                color = st.selectbox('Color Information', options = [None] + list(result.columns), key='color')
                                size = st.selectbox('Color Information', options = [None] + list(result.columns), key='size')
                                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size = size)
                                st.plotly_chart(fig)
                        elif(graphs == 'pie'):
                                values = st.selectbox('Choose Numerical Values', options=list(result.columns))
                                names = st.selectbox('Choose labels', options=list(result.columns))
                                fig = px.pie(data_frame=result, values=values, names=names)
                                st.plotly_chart(fig)
                        elif(graphs == 'sunburst'):
                                path = st.multiselect('Choose your Ptah', options = list(result.columns))
                                fig = px.sunburst(data_frame=result, path=path, values='newcol')
                                st.plotly_chart(fig)
