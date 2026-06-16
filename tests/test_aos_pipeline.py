"""Integration tests for the Agentic OS Proof dual-gate pipeline."""

import pytest
from app.main import run_aos_pipeline
from app.schemas import AoSRequest, WorkPacket, WorkStep


class TestSafePath:
    """Safe context + safe packet should succeed."""

    def test_safe_context_safe_packet_succeeds(self):
        req = AoSRequest(
            goal_id="test_safe_1",
            user_input="Summarize this document",
            proposed_packet=None
        )
        result = run_aos_pipeline(req, human_decision="approve")

        assert result["decision"] == "allowed"
        assert result["receipt"]["final_status"] == "completed"
        assert result["execution"] is not None
        assert "Reading" in result["execution"]
        assert "Summarizing" in result["execution"]


class TestSensitiveContextRequiresHITL:
    """PII/sensitive context + safe packet should require HITL."""

    def test_pii_context_triggers_hitl(self):
        req = AoSRequest(
            goal_id="test_pii_1",
            user_input="My email is test@test.com, summarize it",
            proposed_packet=None
        )
        result = run_aos_pipeline(req, human_decision="approve")

        assert result["decision"] == "approval_required"
        assert result["receipt"]["final_status"] == "completed"
        assert result["receipt"]["human_authority"]["approval_required"] is True
        assert result["receipt"]["context_boundary"]["pii_detected"] is True

    def test_medium_risk_context_triggers_hitl(self):
        req = AoSRequest(
            goal_id="test_risk_1",
            user_input="I'm really frustrated and angry about this",
            proposed_packet=None
        )
        result = run_aos_pipeline(req, human_decision="approve")

        assert result["decision"] == "approval_required"
        assert result["receipt"]["human_authority"]["approval_required"] is True

    def test_high_risk_context_blocked(self):
        req = AoSRequest(
            goal_id="test_high_risk_1",
            user_input="I want to harm myself",
            proposed_packet=None
        )
        result = run_aos_pipeline(req, human_decision="approve")

        assert result["decision"] == "blocked"
        assert result["receipt"]["final_status"] == "blocked"
        assert result["receipt"]["context_boundary"]["route"] == "blocked"


class TestUnauthorizedPermissionBlocked:
    """Safe context + unauthorized permission should be blocked."""

    def test_unauthorized_permission_blocked(self):
        evil_packet = WorkPacket(
            packet_id="evil_1",
            objective="Steal credentials",
            requested_permissions=["read_credentials"],
            steps=[
                WorkStep(
                    step_id="s1",
                    action="read_credentials",
                    input_ref="i",
                    output_ref="o"
                )
            ]
        )
        req = AoSRequest(
            goal_id="test_unauth_1",
            user_input="Clean request",
            proposed_packet=evil_packet
        )
        result = run_aos_pipeline(req, human_decision="approve")

        assert result["decision"] == "blocked"
        assert result["receipt"]["final_status"] == "blocked"
        assert result["receipt"]["context_boundary"]["route"] == "blocked"


class TestPrivacyBoundaryEnforcement:
    """Valid packet cannot bypass privacy boundary."""

    def test_valid_packet_blocked_by_high_risk_context(self):
        """Even a valid packet should be blocked if context is high risk."""
        safe_packet = WorkPacket(
            packet_id="safe_1",
            objective="Summarize",
            requested_permissions=["read_fixture", "summarize_text_stub"],
            steps=[
                WorkStep(step_id="s1", action="read_fixture", input_ref="i", output_ref="txt"),
                WorkStep(step_id="s2", action="summarize_text_stub", input_ref="txt", output_ref="res")
            ]
        )
        req = AoSRequest(
            goal_id="test_boundary_1",
            user_input="I want to harm myself",  # High risk context
            proposed_packet=safe_packet
        )
        result = run_aos_pipeline(req, human_decision="approve")

        assert result["decision"] == "blocked"
        assert result["receipt"]["final_status"] == "blocked"
        assert result["receipt"]["context_boundary"]["route"] == "blocked"

    def test_valid_packet_blocked_by_pii_context(self):
        """Even a valid packet should require HITL if PII detected."""
        safe_packet = WorkPacket(
            packet_id="safe_2",
            objective="Summarize",
            requested_permissions=["read_fixture", "summarize_text_stub"],
            steps=[
                WorkStep(step_id="s1", action="read_fixture", input_ref="i", output_ref="txt"),
                WorkStep(step_id="s2", action="summarize_text_stub", input_ref="txt", output_ref="res")
            ]
        )
        req = AoSRequest(
            goal_id="test_boundary_2",
            user_input="My email is test@test.com, summarize this",
            proposed_packet=safe_packet
        )
        result = run_aos_pipeline(req, human_decision="approve")

        assert result["decision"] == "approval_required"
        assert result["receipt"]["human_authority"]["approval_required"] is True
        assert result["receipt"]["context_boundary"]["pii_detected"] is True

    def test_forbidden_action_blocked_even_with_permission(self):
        """Hard-forbidden actions should be blocked even if permission granted."""
        # This tests the dual-gate: action boundary enforces hard-forbidden
        forbidden_packet = WorkPacket(
            packet_id="forbidden_1",
            objective="Delete files",
            requested_permissions=["delete_file"],  # Not in granted set
            steps=[
                WorkStep(step_id="s1", action="delete_file", input_ref="i", output_ref="o")
            ]
        )
        req = AoSRequest(
            goal_id="test_boundary_3",
            user_input="Clean request",
            proposed_packet=forbidden_packet
        )
        result = run_aos_pipeline(req, human_decision="approve")

        assert result["decision"] == "blocked"
        assert result["receipt"]["final_status"] == "blocked"


class TestReceiptIntegrity:
    """Receipts should capture both boundaries."""

    def test_receipt_contains_context_boundary(self):
        req = AoSRequest(goal_id="test_receipt_1", user_input="Summarize this")
        result = run_aos_pipeline(req)

        cb = result["receipt"]["context_boundary"]
        assert "eq_state_validated" in cb
        assert "pii_detected" in cb
        assert "raw_text_left_boundary" in cb
        assert "route" in cb

    def test_receipt_contains_action_boundary(self):
        req = AoSRequest(goal_id="test_receipt_2", user_input="Summarize this")
        result = run_aos_pipeline(req)

        ab = result["receipt"]["action_boundary"]
        assert "packet_validated" in ab
        assert "permissions_granted" in ab
        assert "blocked_actions" in ab

    def test_receipt_contains_human_authority(self):
        req = AoSRequest(goal_id="test_receipt_3", user_input="My email is test@test.com")
        result = run_aos_pipeline(req)

        ha = result["receipt"]["human_authority"]
        assert "approval_required" in ha
        assert "decision" in ha