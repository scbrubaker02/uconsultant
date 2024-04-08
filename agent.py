from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
from tools import UdacityCatalogSearch


def get_invoke_fn():
    load_dotenv()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a solution architect at Udacity who helps clients assemble sequences of courses to achieve their learning goals."),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    search = UdacityCatalogSearch(max_results=20)

    tools = [search]

    # Only certain models support this
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

    # Construct the OpenAI Tools agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    message_history = ChatMessageHistory()

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        # This is needed because in most real world scenarios, a session id is needed
        # It isn't really used here because we are using a simple in memory ChatMessageHistory
        lambda session_id: message_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    def invoke_fn(input):
        return agent_with_chat_history.invoke({"input": input}, config={"configurable": {"session_id": "<foo>"}})

    # Return a function that invokes the agent with a query
    return invoke_fn
