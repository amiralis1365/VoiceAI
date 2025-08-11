from dotenv import load_dotenv

from livekit.agents import Agent, function_tool, RunContext, get_job_context

from models import MySessionInfo

load_dotenv()

class AboutUsAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=f"""
            You are Jennifer, a friendly and professional customer service representative for a plumbing company. You always speak in english.
            You are currently on a live call with a client.

            You should answer the client's question about the company
        """)

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions="""
            Greet the user, introduce yourself and ask them how you can help them.
            You should always speak in english.
        """)

    @function_tool()
    async def answer_client_question(self, context: RunContext[MySessionInfo], question: str):
        """Use this tool to answer the client's question."""
        context.userdata.question = question
        await self.session.generate_reply(instructions="We are a plumbing company in San Francisco, California. We are open from 9:00 AM to 5:00 PM. We are a family owned and operated business.")
        await self.session.generate_reply(instructions="Ask client if they have any other questions.")
        
    @function_tool()
    async def end_call(self):
        await self.session.generate_reply(instructions="Thank you for calling. Goodbye.")
        get_job_context().shutdown("done")