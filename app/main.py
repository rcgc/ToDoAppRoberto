import streamlit as st

from utils.utils import get_tasks, save_task, Task, TaskStatus

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

def show_tasks_by_status(status: TaskStatus):
    tasks = [task for task in st.session_state.tasks if task.get("status", "") == status.value]

    if status == TaskStatus.PENDING:
        st.warning("PENDING", icon="⚠️")
    elif status == TaskStatus.IN_PROGRESS:
        st.info("In progress", icon="📌")
    else:
        st.success("Complete", icon="✅")

    for task in tasks:
        task_id = task.get("id", "")

        with st.expander(task.get("title", ""), expanded=False):
            st.markdown(f":green[{task.get("timestamp", "")}]")
            st.write(task.get("description", ""))


def show_tasks():
    col_pending, col_in_progress, col_completed = st.columns(3)

    with col_pending:
        show_tasks_by_status(TaskStatus.PENDING)

    with col_in_progress:
        show_tasks_by_status(TaskStatus.IN_PROGRESS)

    with col_completed:
        show_tasks_by_status(TaskStatus.COMPLETED)

def main():
    st.header("To Do App")

    show_add_form()
    show_tasks()


if __name__ == "__main__":
    main()