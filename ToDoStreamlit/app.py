import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
from db_fxns import *

import plotly.express as px

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """




def main():
    stc.html(HTML_BANNER)

    menu = ['CREATE','READ','UPDATE','DELETE','ABOUT']

    choice = st.sidebar.selectbox("Menu",menu)

    create_table()

    if choice == "CREATE":
        st.subheader("Add Item")
        col1 ,col2 = st.columns(2)

        with col1:
            task = st.text_area("Task To Do")
        
        with col2:
            task_status = st.selectbox("Status",["ToDo","Doing","Done"])
            task_due_date = st.date_input("Due Date")
            # task_due_time = st.time_input("Time of task")

        if st.button("Add Task"):
            add_data(task,task_status,task_due_date)
            st.success("Added ::{} ::To Task".format(task))
    
    elif choice == "READ":

        with st.expander("View All"):
            result = view_all_data()
            clean_df  = pd.DataFrame(result,columns=["Task","Status","Date"])
            st.dataframe(clean_df)
        with st.expander("Task Status"):
            task_df = clean_df['Status'].value_counts().to_frame()

            task_df = task_df.reset_index()

            st.dataframe(task_df)

            p1 = px.pie(task_df,names=task_df.index,values = 'Status')
            st.plotly_chart(p1,use_container_width=True)    
    elif choice == "UPDATE":
        st.subheader("Edit Items")
        with st.expander("Current Data"):
            result = view_all_data()

            clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
            st.dataframe(clean_df)

        list_of_tasks = [i[0] for i in view_all_task_names()]
        selected_task = st.selectbox("Task",list_of_tasks)
        task_result = get_task(selected_task)

        if task_result:
            task = task_result[0][0]
            task_status = task_result[0][1]
            task_due_date = task_result[0][2]

            col1, col2 = st.columns(2)

            with col1:
                new_task = st.text_area("Task To Do", task)
            
            with col2:
                new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])

                new_task_due_date = st.date_input(task_due_date)

            
            if st.button("Update Task"):
                edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
                st.success("Update ::{} ::To {}".format(task,new_task))
            
            with st.expander("View Updated Data"):
                result = view_all_data()

                clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
                st.dataframe(clean_df)
if __name__ == "__main__":
    main()