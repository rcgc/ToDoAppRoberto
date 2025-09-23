import streamlit as st

from utils.utils import get_tasks, save_tasks, Task, TaskStatus

if "tasks" not in st.session_state:
    st.session_state["tasks"] = get_tasks()

def add_task(title:str, description:str):
    task = Task(
        id = len(st.session_state.tasks) + 1,
        title = title,
        description = description
    )

    st.session_state.tasks.append(task.model_dump())
    save_tasks(st.session_state.tasks)

def show_add_form():
    with st.expander("Agregar tarea", expanded=True):
        title       = st.text_input("Título")
        description = st.text_area("Descripción")

        if st.button("Agregar", key="btn_add"):
            add_task(title, description)

def update_task(task: Task):
    index = st.session_state.tasks.index(task)

    st.session_state.tasks[index] = task

    save_tasks(st.session_state.tasks)

    st.rerun()

def delete_task(task: Task):
    st.session_state.tasks.remove(task)

    save_tasks(st.session_state.tasks)
    st.rerun()

@st.dialog("Edit Task")
def edit_task(task: Task):
    title       = st.text_input("Titulo", value=task.get("title", ""), key="task_title")
    description = st.text_area("Descripción", value=task.get("description", ""), key="task_description")

    col_save, col_delete = st.columns(2)

    with col_save:
        if st.button("Save changes", type="primary"):
            task["title"] = title
            task["description"] = description

            update_task(task)
    
    with col_delete:
        if st.button("Delete", key="delete_btn"):
            delete_task(task)

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

            if status == TaskStatus.PENDING or status == TaskStatus.IN_PROGRESS:
                col_done_btn, col_edit_btn = st.columns(2)

                with col_done_btn:
                    if st.button("Done", type="primary" if status == TaskStatus.IN_PROGRESS else "secondary", use_container_width=True, key=f"btn_done_{task_id}"):
                        task["status"] = TaskStatus.COMPLETED.value
                        update_task(task)

                with col_edit_btn:
                    if st.button("Edit", use_container_width=True, key=f"btn_edit_{task_id}"):
                        edit_task(task)


                if status == TaskStatus.PENDING:
                    if st.button("Start", type="primary", use_container_width=True, key=f"btn_start_{task_id}"):
                        task["status"] = TaskStatus.IN_PROGRESS.value
                        update_task(task)

            else:
                if st.button("Delete", icon="🗑️", type="primary", key=f"delete_{task_id}"):
                    delete_task(task)

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