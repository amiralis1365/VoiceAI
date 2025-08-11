from dotenv import load_dotenv

from livekit.agents import Agent, function_tool, RunContext, get_job_context

from models import MySessionInfo

load_dotenv()

class FeedbackAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=f"""
            You are Jennifer, a friendly and professional customer service representative for a plumbing company. You always speak in english.
            You are currently on a live call with a client.

            Your goal is to record the client's feedback.
            Ask them to share their feedback.
            Ask them for ellaboration if needed.
            And finally, record all of client feedback.
        """)

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions="""
            Greet the user, introduce yourself and ask them how you can help them.
            You should always speak in english.
        """)

    @function_tool()
    async def record_feedback(self, context: RunContext[MySessionInfo], feedback: str):
        """Use this tool to record the client's feedback."""
        context.userdata.feedback = feedback
        return "Feedback recorded"

    @function_tool()
    async def end_call(self):
        await self.session.generate_reply(instructions="Thank you for calling. Goodbye.")
        get_job_context().shutdown("done")