import os
from logic.rule import Rule


def remove_suffix(function_string):
    """Remove the suffixes."""
    fn_str = function_string.replace("_predicate_fn", "")
    fn_str = fn_str.replace("_time_fn", "")
    fn_str = fn_str.replace("_alert_fn", "")
    return fn_str


def assert_rules_are_well_formed(member_functions):
    """Performs checks.
    `member_functions` is a list of tuples from `get_members(<file>, isfunction)`.
    """
    function_names = [fn_tup[0] for fn_tup in member_functions]

    # 1. Make sure that they are all either predicate or time functions.
    for name in function_names:
        try:
            assert (
                name.endswith("_predicate_fn")
                or name.endswith("_time_fn")
                or name.endswith("_alert_fn")
            )
        except AssertionError:
            raise AssertionError(
                "Function `{}` does not conform to the protocol. All functions need to have end in one of: predicate_fn, time_fn, or alert_fn. Check your definitions.py.".format(
                    name
                )
            )

    # 2. Make sure that there is exactly one predicate and one time function per
    # rule.
    unique_function_names = set(function_names)
    unique_function_names = [remove_suffix(name) for name in unique_function_names]
    for name in unique_function_names:
        assert (
            name + "_predicate_fn"
        ) in function_names, "No predicate function found for `{}` rule.".format(name)
        assert (
            name + "_time_fn"
        ) in function_names, "No time function found for `{}` rule.".format(name)
        assert (
            name + "_alert_fn"
        ) in function_names, "No alert function found for `{}` rule.".format(name)

    # 3. Check environment variables to make sure everything is there.
    env_vars_to_check = [
        "TWILIO_SID",
        "TWILIO_AUTH",
        "TWILIO_PHONE_FROM",
        "TWILIO_PHONE_TO",
    ]
    for var in env_vars_to_check:
        if var not in os.environ:
            print("{} not found in .env. Proceed with caution.".format(var))


def create_rules_from_functions(definition_functions):
    """Creates `Rule` objects from functions."""
    assert_rules_are_well_formed(definition_functions)
    definition_dict = {fn_tup[0]: fn_tup[1] for fn_tup in definition_functions}
    unique_rule_names = set(
        [remove_suffix(item) for item in list(definition_dict.keys())]
    )
    rules = []
    for rule_name in unique_rule_names:
        predicate_fn = definition_dict[rule_name + "_predicate_fn"]
        time_fn = definition_dict[rule_name + "_time_fn"]
        alert_fn = definition_dict[rule_name + "_alert_fn"]
        rule = Rule(predicate_fn, time_fn, alert_fn)
        rules.append(rule)
    return rules