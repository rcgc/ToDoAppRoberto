import streamlit as st

from utils.utils import get_tasks, save_task, Task

if "tasks" not in st.session_state:
    st.session_state["tasks"] = get_tasks()

def add_task(title:str, description:str):
    task = Task(
        id = len(st.session_state.tasks) + 1,
        title = title,
        description = description
    )

    st.session_state.tasks.append(task.model_dump())
    save_task(st.session_state.tasks)

def show_add_form():
    with st.expander("Agregar tarea", expanded=True):
        title       = st.text_input("Título")
        description = st.text_area("Descripción")

        if st.button("Agregar"):
            add_task(title, description)

def main():
    st.header("To Do App")

    show_add_form()


if __name__ == "__main__":
    main()