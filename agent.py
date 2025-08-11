from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool, RunContext, get_job_context
from livekit.plugins import openai, noise_cancellation
from openai.types.beta.realtime.session import TurnDetection

from models import MySessionInfo, TaskType
from agents.plumber import PlumberAgent
from agents.feedback import FeedbackAgent
from agents.aboutus import AboutUsAgent
from agents.admin import AdminAgent

load_dotenv()

class Operator(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=f"""
            You are Anna, a friendly and professional customer service representative for a plumbing company.
            You are currently on a live call with a client.

            Your goal is to connect client to the right agent:
            - If the client is asking for a plumber, connect them to the plumber agent.
            - If the client wants to give feedback, connect them to the feedback agent.
            - If the client wants to know about the company, connect them to about us agent.
            - If the caller is the system admin, authenticate them and connect them to the system admin agent.
        """)

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions="""
            Greet the user, introduce yourself and ask them how you can help them.\
            You should always speak in english.
        """)

    @function_tool()
    async def transfer_call_to_plumber_agent(self, context: RunContext[MySessionInfo]):
        """ Use this tool to transfer the call to the plumber agent. """
        context.userdata.task = TaskType.PLUMBER
        return "Transfer call to plumber agent", PlumberAgent()

    @function_tool()
    async def transfer_call_to_feedback_agent(self, context: RunContext[MySessionInfo]):
        """ Use this tool to transfer the call to the feedback agent. """
        context.userdata.task = TaskType.FEEDBACK
        return "Transfer call to feedback agent", FeedbackAgent()

    @function_tool()
    async def transfer_call_to_about_us_agent(self, context: RunContext[MySessionInfo]):
        """ Use this tool to transfer the call to the about us agent. """
        context.userdata.task = TaskType.ABOUT_US
        return "Transfer call to about us agent", AboutUsAgent()

    @function_tool()
    async def transfer_call_to_admin_agent(self, context: RunContext[MySessionInfo], password: str):
        """ Use this tool to transfer the call to the admin agent. 
            Args:
                password: The password to authenticate the admin.
        """
        print({"password": password})
        if password != "1234":
            await self.session.generate_reply(instructions="Invalid password.")
            await self.session.generate_reply(instructions="Thank you for calling. Goodbye.")
            return "End call"
        context.userdata.task = TaskType.SYSTEM_ADMIN
        return "Transfer call to admin agent", AdminAgent()


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession[MySessionInfo](
        userdata=MySessionInfo(),
        llm=openai.realtime.RealtimeModel(
            voice="coral",
            model="gpt-4o-realtime-preview",
            turn_detection=TurnDetection(
                type="semantic_vad",
                eagerness="auto",
                create_response=True,
                interrupt_response=True,
            )
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Operator(),
        room_input_options=RoomInputOptions(
            # Enable noise cancellation for better audio quality
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))