import os

from dotenv import load_dotenv

from typing import List

from pydantic import BaseModel, Field

from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser

load_dotenv("../.env")

model = ChatGroq(

    model="openai/gpt-oss-120b",

    temperature=0,

    groq_api_key=os.environ.get("GROQ_API_KEY"),

)

review_parser = PydanticOutputParser(

    pydantic_object=BaseModel,

)

class ReviewOutput(BaseModel):

    complaints: List[str] = Field(default_factory=list, description="List of complaints in the review.")

    product_feature: str = Field(default="", description="The product or feature in the review.")

    customer_sentiment: str = Field(default="", description="The sentiment by the customer (positive, negative, neutral).")


parser1 = PydanticOutputParser(pydantic_object=ReviewOutput)

parser2 = StrOutputParser()


STEP1_PROMPT = PromptTemplate(
    template="""

Extract product or feature, Complaint and sentiment.

{json_formatting}

{review}

""",

    input_variables=["review"],

    partial_variables={
        "json_formatting": parser1.get_format_instructions()
    },

)


print("Enter raw customer review:")

customer_review = input()


STEP2_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "you are a ticket writter"),
    ("human", "create ticket based on given info {information}"),
])


chain = STEP1_PROMPT | model | parser1 | STEP2_PROMPT | model | parser2

output = chain.invoke({"review": customer_review})

print(output)