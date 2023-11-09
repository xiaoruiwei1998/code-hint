system_message = """
Fix the provided Python [user-code] based on the provided [task-description] and [sample-solution] and generate [fixed-code]. 
The [fixed-code] should follow the existing solving strategy and solution path in [user-code], use the same type of [control_structures], use the same variable names as [user-code] and requires the least amount of edits from the [user-code].
For example, the [user-code] uses [control_structures], the [fixed-code] should also these [control_structures].
The [fixed-code] should pass the provided [unittest-code] and be more similar to the [user-code] than the [sample-solution].
The [fixed-code] should follow the Python style guide.
[task-description]: '{question_description}'
[end-task-description]

[sample-solution]: '{Example_student_solution}'
[end-solution]

[unittest-code]: '{unittest_code}'
[end-unittest-code]

[control-structures]: '{control_structures}'
"""

# user message here is the example student answer
user_message = """[user-code]:
{Example_buggy_code}
[end-user-code]"""

assistant_message = """[fixed-code]:
{Example_fixed_code}
[end-fixed-code]"""


def build_code_prompt(question_line, buggy_code, system_message=system_message,user_message=user_message,assistant_message=assistant_message):
    control_structures = find_control_structures(buggy_code)
    system_message = system_message.format(
        question_description
        Example_student_solution
        unittest_code
        control_structures
    )
    user_message = user_message.format(
        Example_buggy_code
    )
    assistant_message = assistant_message.format(
        Example_fixed_code
    )
    prompt_code = "[user-code]:\n" + buggy_code + "\n[end-user-code]"
    prompt_messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_message},
                {"role": "user", "content": prompt_code},
            ]
    #print("prompt_messages here: \n", prompt_messages)
    return prompt_messages