"""Contains the class `Agent`, the core of the system."""
from src.agent.llm import LLM
from src.agent.knowledge import Store
from src.agent.memory import Memory, Message, Role
from src.agent.prompts import PROMPTS


class Agent:
    """Penetration Testing Assistant"""

    def __init__(self, model: str, tools_docs: str, knowledge_base: Store = None):
        # Agent Components
        self.llm = LLM(model=model)
        self.mem = Memory()
        self.vdb: Store | None = knowledge_base

        # Prompts
        self._available_tools = tools_docs
        self.system_plan_gen = PROMPTS[model]['plan']['system']
        self.user_plan_gen = PROMPTS[model]['plan']['user']
        self.system_plan_con = PROMPTS[model]['plan_conversion']['system']
        self.user_plan_con = PROMPTS[model]['plan_conversion']['user']

    def query(self, sid: int, user_in: str, rag=True, stream=True):
        """Performs a query to the Large Language Model, set `rag=True`
        to leverage Retrieval Augmented Generation."""
        context = ''
        if rag:
            context = self._retrieve(user_in)

        # user prompt
        prompt = self.user_plan_gen.format(user_input=user_in, tools=self._available_tools, context=context)
        self.mem.store_message(
            sid,
            Message(Role.USER, prompt)
        )
        messages = self.mem.get_session(sid).messages_to_dict_list()

        # generate response
        response = ''
        prompt_tokens = 0
        response_tokens = 0
        for chunk in self.llm.query(messages):
            if chunk['done']:
                prompt_tokens = chunk['prompt_eval_count']
                response_tokens = chunk['eval_count']
            yield chunk['message']['content']

            response += chunk['message']['content']

        self.mem.get_session(sid).messages[-1].tokens = prompt_tokens
        self.mem.store_message(
            sid,
            Message(Role.ASSISTANT, response, tokens=response_tokens)
        )

    def execute_plan(self, sid):
        """Executes the last plan stored in memory"""

    def new_session(self, sid: int):
        """Initializes a new conversation"""
        self.mem.store_message(sid, Message(Role.SYS, self.system_plan_gen))

    def get_session(self, sid: int):
        """Open existing conversation"""
        return self.mem.get_session(sid)

    def save_session(self, sid: int):
        """Saves the specified session to JSON"""
        self.mem.save_session(sid)

    def delete_session(self, sid: int):
        """Deletes the specified session"""
        self.mem.delete_session(sid)

    def rename_session(self, sid: int, session_name: str):
        """Rename the specified session"""
        self.mem.rename_session(sid, session_name)

    def _retrieve(self, user_in: str):
        """Get context from Qdrant"""
        if not self.vdb:
            raise RuntimeError('Trying to use Agent with RAG but it is not initialized')
        context = ''
        for retrieved in self.vdb.retrieve(user_in):
            context += (f"{retrieved.payload['title']}:"
                        f"\n{retrieved.payload['text']}\n\n")
        return context


if __name__ == '__main__':
    from src.agent.knowledge.routing import LLMRouter

    # vector_db = Store(router=LLMRouter())
    agent = Agent(model='llama3', tools_docs='')  # , knowledge_base=vector_db)

    user_query = 'what are most common authentication issues in websites?'
    # user_query = 'How do I perform host discovery with nmap?'

    for chunk in agent.query(1, user_query, rag=False):
        print(chunk, end='')
    print(f'Tokens used: {agent.get_session(1).token_length()}')
