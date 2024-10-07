import pandas as pd
from llama_index.core.llama_dataset import (
    LabelledRagDataset,
    CreatedBy,
    CreatedByType,
    LabelledRagDataExample,
)

data = [
    [
        "Should I always use parentheses around tuples?",
        "Use parentheses sparingly.  It is fine, though not required, to use parentheses around tuples. Do not use them in return statements or conditional statements unless using parentheses for implied line continuation or to indicate a tuple.",
        "No, you do not have to use parentheses around tuples, but you can if you want.",
    ],
    [
        "What are the benefits and drawbacks of using decorators?",
        "Elegantly specifies some transformation on a method; the transformation might eliminate some repetitive code, enforce invariants, etc.  Decorators can perform arbitrary operations on a function's arguments or return values, resulting in surprising implicit behavior. Additionally, decorators execute at object definition time. For module-level objects (classes, module functions, ...) this happens at import time. Failures in decorator code are pretty much impossible to recover from.",
        "Decorators can reduce repetitive code, and enforce invariants.  However, they may return surprising results.  Applications are not able to recover from errors in decorators.",
    ],
    [
        "How long can a docstring be?",
        "A docstring should be organized as a summary line (one physical line not exceeding 80 characters) terminated by a period, question mark, or exclamation point. When writing more (encouraged), this must be followed by a blank line, followed by the rest of the docstring starting at the same cursor position as the first quote of the first line. There are more formatting guidelines for docstrings below.",
        "A docstring can span multiple lines, but each line should be no more than 80 characters.",
    ],
    [
        "Does punctuation and grammar matter in comments?",
        "Comments should be as readable as narrative text, with proper capitalization and punctuation. In many cases, complete sentences are more readable than sentence fragments. Shorter comments, such as comments at the end of a line of code, can sometimes be less formal, but you should be consistent with your style.  Although it can be frustrating to have a code reviewer point out that you are using a comma when you should be using a semicolon, it is very important that source code maintain a high level of clarity and readability. Proper punctuation, spelling, and grammar help with that goal.",
        "Yes, adhering to basic grammar and punctuation make code comments more readable.",
    ],
    [
        "Should I use tabs or spaces to indent my code?",
        "Indent your code blocks with 4 spaces. Never use tabs. Implied line continuation should align wrapped elements vertically (see line length examples), or use a hanging 4-space indent. Closing (round, square or curly) brackets can be placed at the end of the expression, or on separate lines, but then should be indented the same as the line with the corresponding opening bracket.",
        "Use 4 spaces to indent a line of code.",
    ],
    [
        "I like to use blank lines to separate things.  Are there any guidelines about blank lines?",
        "Two blank lines between top-level definitions, be they function or class definitions. One blank line between method definitions and between the docstring of a class and the first method. No blank line following a def line. Use single blank lines as you judge appropriate within functions or methods.",
        "Sure, you can use two blank lines to separate top-level items, like functions.  One blank line is conventional between methods and after a docstring.  No blank line is necessary after a function definition.  You can also add single blank lines at your discretion.",
    ],
    [
        "Should I use absolute imports or relative imports?",
        "Do not use relative names in imports. Even if the module is in the same package, use the full package name. This helps prevent unintentionally importing a package twice.",
        "You shouldn’t use relative imports.",
    ],
    [
        "What are TODO comments?",
        "Use TODO comments for code that is temporary, a short-term solution, or good-enough but not perfect.A TODO comment begins with the word TODO in all caps, a following colon, and a link to a resource that contains the context, ideally a bug reference. A bug reference is preferable because bugs are tracked and have follow-up comments. Follow this piece of context with an explanatory string introduced with a hyphen -. The purpose is to have a consistent TODO format that can be searched to find out how to get more details.",
        "Comments that describe code that is temporary or acceptable, but not perfect.",
    ],
    [
        "Should I use type hints?",
        "Type annotations improve the readability and maintainability of your code.  The type checker will convert many runtime errors to build-time errors, and reduce your ability to use Power Features.You are strongly encouraged to enable Python type analysis when updating code. When adding or modifying public APIs, include type annotations and enable checking via pytype in the build system. As static analysis is relatively new to Python, we acknowledge that undesired side-effects (such as wrongly inferred types) may prevent adoption by some projects. In those situations, authors are encouraged to add a comment with a TODO or link to a bug describing the issue(s) currently preventing type annotation adoption in the BUILD file or in the code itself as appropriate.",
        "Yes, it is recommended that you use type annotations because they improve readability and maintainability of your code.",
    ],
    [
        "In Javascript, I end lines with semi-colons.  Can I do that in Python?",
        "Do not terminate your lines with semicolons, and do not use semicolons to put two statements on the same line.",
        "No, you should not end lines with semi-colons.",
    ],
    [
        "Can I leave a file open so I can use it later?",
        "Explicitly close files and sockets when done with them. This rule naturally extends to closeable resources that internally use sockets, such as database connections, and also other resources that need to be closed down in a similar fashion. To name only a few examples, this also includes mmap mappings, h5py File objects, and matplotlib.pyplot figure windows.",
        "You should close a file after you’ve used it.",
    ],
]

# df = pd.read_csv("test.csv")

df = pd.DataFrame(data, columns=["query", "reference_contexts", "reference_answer"])

labeled_examples = []

for index, row in df.iterrows():
    query = row["query"]
    reference_context = row["reference_contexts"]
    reference_answer = row["reference_answer"]

    example = LabelledRagDataExample(
        query=query,
        query_by=CreatedBy(type=CreatedByType.HUMAN),
        reference_answer=reference_answer,
        reference_contexts=[reference_context],
        reference_by=CreatedBy(type=CreatedByType.HUMAN),
    )

    labeled_examples.append(example)


rag_test_dataset = LabelledRagDataset(examples=labeled_examples)


rag_test_dataset.save_json("style_guide_test.json")
