import streamlit as st

from rag import create_rag_chain


st.set_page_config(
    page_title="Hospital Assistant",
)


st.title("دستیار بیمارستان میلاد")


@st.cache_resource
def load_chain():

    return create_rag_chain()



chain = load_chain()



question = st.text_input(
    "سوال خود را بپرسید:"
)


if question:


    with st.spinner("در حال جستجو..."):

        response = chain.invoke(
            {
                "input": question
            }
        )


    st.subheader("پاسخ:")

    st.write(
        response["answer"]
    )


    st.subheader("منابع:")

    for doc in response["context"]:

        st.write(
            doc.metadata["url"]
        )