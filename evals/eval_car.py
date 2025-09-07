from arcade_tdk import ToolCatalog
from arcade_evals import (
    EvalRubric,
    EvalSuite,
    ExpectedToolCall,
    tool_eval,
)
from arcade_evals.critic import SimilarityCritic

import tessie
from tessie.tools.car import get_location, get_battery

# Evaluation rubric
rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
)

catalog = ToolCatalog()
catalog.add_module(tessie)

@tool_eval()
def car_eval_suite() -> EvalSuite:
    suite = EvalSuite(
        name="Car Tools Evaluation",
        system_message=(
            "You are an AI assistant with access to Tesla car tools. "
            "Use them to help the user get information about their vehicle."
        ),
        catalog=catalog,
        rubric=rubric,
    )

    suite.add_case(
        name="Get car location by VIN",
        user_message="What's the current location of the car with VIN 5YJSA1E26HF123456?",
        expected_tool_calls=[ExpectedToolCall(func=get_location, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Get battery level by VIN",
        user_message="Check the battery level for vehicle 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=get_battery, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Get location for Tesla Model S",
        user_message="I need to find where my Tesla Model S is parked. The VIN is 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=get_location, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Check battery status before trip",
        user_message="Before I start my road trip, can you check the battery status of my car? VIN is 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=get_battery, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Get both location and battery info",
        user_message="I need to know where my car is and what the battery level is. VIN: 5YJSA1E26HF123456.",
        expected_tool_calls=[
            ExpectedToolCall(func=get_location, args={"vin": "5YJSA1E26HF123456"}),
            ExpectedToolCall(func=get_battery, args={"vin": "5YJSA1E26HF123456"})
        ],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.7),
        ]
    )

    return suite