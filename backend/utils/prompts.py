from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.prompts.prompt_type import PromptType

topic = "python programming style"

HYDE_TMPL = (
    f"The source documents the user expects to use are related to {topic}"
    "Please write a passage to answer the question\n"
    "Try to include as many key details as possible.\n"
    "\n"
    "\n"
    "{context_str}\n"
    "\n"
    "\n"
    'Passage:"""\n'
)

CUSTOM_HYDE_PROMPT = PromptTemplate(HYDE_TMPL, prompt_type=PromptType.SUMMARY)


SELF_REFLECTION_PROMPT = f"""
You are the last reviewer before a Proposed Answer to a User Query goes out.
The source documents provided to you are about {topic}.
Evaluate whether the Proposed Answer is an accurate, relevant, related response to the User Query.
If the Proposed Answer is relevant and accurate, respond "Yes".  If not, respond "No".
If the Query is not related to the Source Document Topic, respond "No".
Do not elaborate; only respond with "Yes" or "No".

Source Document Topic
{topic}

User Query
{{query}}

Proposed Answer
{{response}}
"""
