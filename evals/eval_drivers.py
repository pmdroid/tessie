from arcade_tdk import ToolCatalog
from arcade_evals import (
    EvalRubric,
    EvalSuite,
    ExpectedToolCall,
    tool_eval,
)
from arcade_evals.critic import SimilarityCritic

import tessie
from tessie.tools.drivers import list_driver, delete_driver

# Evaluation rubric
rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
)

catalog = ToolCatalog()
catalog.add_module(tessie)

@tool_eval()
def drivers_eval_suite() -> EvalSuite:
    suite = EvalSuite(
        name="Drivers Tools Evaluation",
        system_message=(
            "You are an AI assistant with access to Tesla driver management tools. "
            "Use them to help the user manage authorized drivers for their vehicle."
        ),
        catalog=catalog,
        rubric=rubric,
    )

    suite.add_case(
        name="Get drivers for a vehicle",
        user_message="Show me all the drivers for my Tesla with VIN 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=list_driver, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="List authorized drivers",
        user_message="I need to see who has access to drive my car. VIN is 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=list_driver, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Remove specific driver",
        user_message="Remove driver ID driver_456 with user ID user_789 from my Tesla VIN 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=delete_driver, args={"vin": "5YJSA1E26HF123456", "user_id": "user_789"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.5),
            SimilarityCritic(critic_field="user_id", weight=0.5),
        ]
    )

    suite.add_case(
        name="Check who can drive my car",
        user_message="Who are the current authorized drivers for vehicle VIN 5YJSA1E26HF123456?",
        expected_tool_calls=[ExpectedToolCall(func=list_driver, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Delete driver access",
        user_message="I want to revoke access for driver john_driver with user ID usr_123 from my car VIN 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=delete_driver, args={"vin": "5YJSA1E26HF123456", "user_id": "usr_123"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.5),
            SimilarityCritic(critic_field="user_id", weight=0.5),
        ]
    )

    suite.add_case(
        name="Get driver list for Model S",
        user_message="What drivers are authorized for my Model S? The VIN is 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=list_driver, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Remove unauthorized driver",
        user_message="Please remove the driver with ID temp_driver and user ID temp_123 from vehicle VIN 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=delete_driver, args={"vin": "5YJSA1E26HF123456", "user_id": "temp_123"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.5),
            SimilarityCritic(critic_field="user_id", weight=0.5),
        ]
    )

    return suite