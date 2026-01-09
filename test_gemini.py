from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
    api_key = AIzaSyAHWsYsdTQI0W6OZLBYO-JdlnCIlj2m06g
)

response = llm.invoke("Say Gemini is working")
print(response.content)
