from dotenv import load_dotenv

from livekit.agents import Agent, function_tool, RunContext, get_job_context

from models import MySessionInfo

load_dotenv()

class AdminAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=f"""
            You are Jennifer, a friendly and professional admin service representative for a plumbing company. You always speak in english.
            You are currently on a live call with one of company's admin.

            You should use tools to give information to the admin.
        """)

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions="""
            Greet the user, introduce yourself and ask them how you can help them.
            You should always speak in english.
        """)

    @function_tool()
    async def get_admin_next_schedule(self, context: RunContext[MySessionInfo], question: str):
        """Use this tool to answer the client's question."""
        await self.session.generate_reply(instructions="The admin next schedule is on 12th of August, 2025 at 10:00 AM.")
        return "Next schedule is on 12th of August, 2025 at 10:00 AM."
        
    @function_tool()
    async def end_call(self):
        await self.session.generate_reply(instructions="Thank you for calling. Goodbye.")
        get_job_context().shutdown("done")