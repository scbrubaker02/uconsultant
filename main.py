from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from catalog import search

def document_example():
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)

    ans = document_chain.invoke({
        "input": "how can langsmith help with testing?",
        "context": [Document(page_content="langsmith can let you visualize test results")]
    })

    print(ans)

def agent_example():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a solution architect at Udacity who helps clients assemble sequences of courses to achieve their learning goals."),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    print(prompt.messages)

    tools = [search]

    # Only certain models support this
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

    # Construct the OpenAI Tools agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    r = agent_executor.invoke({"input": "I need a short program of no more than two courses that will upskill my team's understanding of AWS."})
    print(r['output'])

def main():
    # document_example()
    agent_example()

if __name__ == "__main__":
    main()