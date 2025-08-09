from dotenv import load_dotenv
from dataclasses import dataclass
from datetime import datetime

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool, RunContext, get_job_context
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()

@dataclass
class MySessionInfo:
    name: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None
    problem: str | None = None
    appointment_time: datetime | None = None

class Assistant(Agent):
    def __init__(self) -> None:
        today = datetime.now().strftime("%B %d, %Y")
        self.appointment_time_counter = 0
        super().__init__(instructions=f"""
            You are Sarah, a friendly and professional customer service representative for a plumbing company.
            You are currently on a live call with a customer.
            Today is {today}.

            Your goal is to assist the customer in scheduling a plumbing appointment. You must collect four pieces of information, in this order:
                1.	Customer’s name
                2.	The plumbing problem they are experiencing
                3.	The service address
                4.	Preferred appointment date and time (When the appointment date is not clear ask again for clarification.)

            Conversation guidelines:
                •	Speak in a natural, human-like tone—warm, polite, and conversational.
                •	Ask one question at a time and wait for the customer’s full response.
                •	After receiving each piece of information, paraphrase it back to the customer for confirmation before moving on.
                •	Example: “So your name is John Smith, correct?”
                •	Do not continue until the customer confirms.
                •	Use small talk and conversational bridges to make the interaction smooth and natural, rather than sounding like a checklist.
                •	If the customer goes off-topic, politely guide the conversation back on track while keeping the tone friendly.
                •	Once all details are confirmed, clearly restate the appointment details and end the call on a positive note.
        """)

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions="Greet the user, introduce yourself and ask them how you can help them.")
    
    @function_tool()
    async def record_name(self, context: RunContext[MySessionInfo], name: str):
        """Use this tool to record the customer's name."""
        context.userdata.name = name
        await self._end_if_done()
    
    @function_tool()
    async def record_address(self, context: RunContext[MySessionInfo], street: str, city: str, state: str, zip: str):
        """Use this tool to record the customer's address.
        Args:
            street: The street address of the customer.
            city: The city of the customer.
            state: The state of the customer.
            zip: The zip code of the customer.
        """
        context.userdata.street = street
        context.userdata.city = city
        context.userdata.state = state
        context.userdata.zip = zip
        await self._end_if_done()

    @function_tool()
    async def record_problem(self, context: RunContext[MySessionInfo], problem: str):
        """Use this tool to record the customer's problem."""
        context.userdata.problem = problem
        await self._end_if_done()
    
    @function_tool()
    async def record_appointment_time(self, context: RunContext[MySessionInfo], appointment_time: datetime):
        """Use this tool to record the customer's appointment time."""
        if self.appointment_time_counter == 0:
            self.appointment_time_counter += 1
            await self.session.generate_reply(instructions="This time is not available. Please ask customer another time.")
        else:
            context.userdata.appointment_time = appointment_time
            await self._end_if_done()

    async def _end_if_done(self):
        if self.session.userdata.name and self.session.userdata.street and self.session.userdata.city and self.session.userdata.state and self.session.userdata.zip and self.session.userdata.problem and self.session.userdata.appointment_time:
            print(self.session.userdata)
            await self.session.generate_reply(instructions="Thank for calling and say goodbye in a formal manner.")
        else:
            await self.session.generate_reply(instructions="Continue getting user information.")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession[MySessionInfo](
        userdata=MySessionInfo(),
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # Disable noise cancellation for local development
            # noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))