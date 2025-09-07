from arcade_tdk import ToolCatalog
from arcade_evals import (
    EvalRubric,
    EvalSuite,
    ExpectedToolCall,
    tool_eval,
)
from arcade_evals.critic import SimilarityCritic

import tessie
from tessie.tools.invitation import list_invitation, create_invitation, revoke_invitation

# Evaluation rubric
rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
)

catalog = ToolCatalog()
catalog.add_module(tessie)

@tool_eval()
def invitation_eval_suite() -> EvalSuite:
    suite = EvalSuite(
        name="Invitation Tools Evaluation",
        system_message=(
            "You are an AI assistant with access to Tesla invitation management tools. "
            "Use them to help the user manage car sharing invitations."
        ),
        catalog=catalog,
        rubric=rubric,
    )

    suite.add_case(
        name="List invitations for a vehicle",
        user_message="Show me all the invitations for my Tesla with VIN 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=list_invitation, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Create new invitation",
        user_message="I want to create a sharing invitation for my car VIN 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=create_invitation, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Revoke specific invitation",
        user_message="Please revoke the invitation with ID inv_xyz789 for vehicle VIN 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=revoke_invitation, args={"vin": "5YJSA1E26HF123456", "invite_id": "inv_xyz789"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.5),
            SimilarityCritic(critic_field="invite_id", weight=0.5),
        ]
    )

    suite.add_case(
        name="Generate invitation link",
        user_message="Generate a new sharing link for my Model 3, VIN is 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=create_invitation, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    suite.add_case(
        name="Check and create invitation workflow",
        user_message="First check what invitations exist for VIN 5YJSA1E26HF123456, then create a new one.",
        expected_tool_calls=[
            ExpectedToolCall(func=list_invitation, args={"vin": "5YJSA1E26HF123456"}),
            ExpectedToolCall(func=create_invitation, args={"vin": "5YJSA1E26HF123456"})
        ],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.7),
        ]
    )

    suite.add_case(
        name="Remove old invitation",
        user_message="Cancel the invitation invite_abc123 for my Tesla VIN 5YJSA1E26HF123456.",
        expected_tool_calls=[ExpectedToolCall(func=revoke_invitation, args={"vin": "5YJSA1E26HF123456", "invite_id": "invite_abc123"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.5),
            SimilarityCritic(critic_field="invite_id", weight=0.5),
        ]
    )

    suite.add_case(
        name="List all shared access",
        user_message="What sharing invitations are currently active for vehicle VIN 5YJSA1E26HF123456?",
        expected_tool_calls=[ExpectedToolCall(func=list_invitation, args={"vin": "5YJSA1E26HF123456"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="vin", weight=0.8),
        ]
    )

    return suite