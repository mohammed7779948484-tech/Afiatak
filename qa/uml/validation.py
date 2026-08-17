from __future__ import annotations

import re

from engine.core.io import ROOT, load_yaml
from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic

MULTIPLICITY = re.compile(r"^(\*|[0-9]+|[0-9]+\.\.(\*|[0-9]+))$")


def validate_uml(model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    selected = set(view.include)
    relations = [item for item in model.relations if item.id in view.relations]
    elements = model.by_id
    for relation in relations:
        if relation.source not in selected or relation.target not in selected:
            diagnostics.append(
                Diagnostic(
                    "Q3",
                    "hidden-endpoint",
                    "Selected relation endpoint is not visible",
                    subject=relation.id,
                )
            )
    if any(item not in elements for item in view.include) or any(
        relation.source not in elements or relation.target not in elements for relation in relations
    ):
        return diagnostics
    element_types = {
        "use_case": {"actor", "use_case"},
        "class": {"class", "note"},
        "object": {"object"},
        "activity": {"initial", "final", "action", "decision", "merge", "fork", "join", "object", "note"},
        "sequence": {"participant", "actor", "object", "component"},
        "communication": {"participant", "actor", "object", "component"},
        "state": {"initial", "final", "state"},
        "package": {"package"},
        "component": {"component", "provided_interface", "required_interface"},
        "deployment": {"deployment_node"},
    }
    relation_types = {
        "use_case": {"association", "include", "extend", "generalization"},
        "class": {"association", "generalization", "aggregation", "composition"},
        "object": {"association"},
        "activity": {"control_flow", "object_flow"},
        "sequence": {"message", "return_message"},
        "communication": {"message", "return_message"},
        "state": {"transition"},
        "package": {"dependency"},
        "component": {"dependency", "connector", "realization"},
        "deployment": {"communication_path"},
    }
    for item in view.include:
        if elements[item].type not in element_types[view.diagram_type]:
            diagnostics.append(
                Diagnostic(
                    "Q3",
                    "invalid-element-type",
                    f"{elements[item].type} is invalid in a {view.diagram_type} view",
                    subject=item,
                )
            )
    for relation in relations:
        if relation.type not in relation_types[view.diagram_type]:
            diagnostics.append(
                Diagnostic(
                    "Q3",
                    "invalid-relation-type",
                    f"{relation.type} is invalid in a {view.diagram_type} view",
                    subject=relation.id,
                )
            )
    if view.diagram_type == "use_case":
        for relation in relations:
            source_type = elements[relation.source].type
            target_type = elements[relation.target].type
            if relation.type == "association" and {source_type, target_type} != {
                "actor",
                "use_case",
            }:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-association",
                        "Use-case association must join actor and use case",
                        subject=relation.id,
                    )
                )
            if relation.type in {"include", "extend"} and (
                source_type != "use_case" or target_type != "use_case"
            ):
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-use-case-relation",
                        "Include/extend endpoints must be use cases",
                        subject=relation.id,
                    )
                )
            if relation.type == "generalization" and (
                source_type not in {"actor", "use_case"} or source_type != target_type
            ):
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-use-case-generalization",
                        "Generalization must join actors or join use cases",
                        subject=relation.id,
                    )
                )
    if view.diagram_type == "class":
        course = load_yaml(ROOT / "governance" / "course-profile.yaml")
        allowed = set(course["class"]["accepted_relationships"])
        for relation in relations:
            if relation.type not in allowed:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-class-relation",
                        "Unsupported class relation",
                        subject=relation.id,
                    )
                )
            for key in ("sourceMultiplicity", "targetMultiplicity"):
                value = relation.metadata.get(key)
                if value and not MULTIPLICITY.fullmatch(str(value)):
                    diagnostics.append(
                        Diagnostic(
                            "Q3",
                            "invalid-multiplicity",
                            f"Invalid {key}: {value}",
                            subject=relation.id,
                        )
                    )
    if view.diagram_type in {"sequence", "communication"}:
        sequence_values = [relation.metadata.get("sequence") for relation in relations]
        if any(
            not isinstance(value, int) or isinstance(value, bool) or value < 1
            for value in sequence_values
        ):
            diagnostics.append(
                Diagnostic(
                    "Q3",
                    "invalid-message-order",
                    "Interaction sequence values must be positive integers",
                )
            )
        elif len(sequence_values) != len(set(sequence_values)):
            diagnostics.append(
                Diagnostic(
                    "Q3", "duplicate-message-order", "Interaction message order must be unique"
                )
            )
        elif sorted(sequence_values) != list(range(1, len(sequence_values) + 1)):
            diagnostics.append(
                Diagnostic(
                    "Q3",
                    "noncontiguous-message-order",
                    "Interaction message order must be contiguous from 1",
                )
            )
    if view.diagram_type == "state":
        initial = [item for item in view.include if elements[item].type == "initial"]
        if len(initial) != 1:
            diagnostics.append(
                Diagnostic(
                    "Q3", "initial-state-count", "State view requires exactly one initial node"
                )
            )
        for relation in relations:
            if relation.type != "transition" or not relation.name:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-transition",
                        "State relationships must be labeled transitions",
                        subject=relation.id,
                    )
                )
        if len(initial) == 1:
            start = initial[0]
            incoming = {relation.target for relation in relations}
            outgoing = {relation.source for relation in relations}
            if start in incoming:
                diagnostics.append(
                    Diagnostic(
                        "Q3", "initial-incoming", "Initial state cannot have incoming transitions"
                    )
                )
            for item in view.include:
                if elements[item].type == "final" and item in outgoing:
                    diagnostics.append(
                        Diagnostic(
                            "Q3",
                            "final-outgoing",
                            "Final state cannot have outgoing transitions",
                            subject=item,
                        )
                    )
            reachable = {start}
            changed = True
            while changed:
                changed = False
                for relation in relations:
                    if relation.source in reachable and relation.target not in reachable:
                        reachable.add(relation.target)
                        changed = True
            for item in set(view.include) - reachable:
                diagnostics.append(
                    Diagnostic(
                        "Q3", "unreachable-state", "State is unreachable from initial", subject=item
                    )
                )
    if view.diagram_type == "activity":
        initial = [item for item in view.include if elements[item].type == "initial"]
        final = [item for item in view.include if elements[item].type == "final"]
        if len(initial) != 1 or not final:
            diagnostics.append(
                Diagnostic(
                    "Q3",
                    "activity-endpoints",
                    "Activity requires one initial and at least one final node",
                )
            )
        for relation in relations:
            if relation.type not in {"control_flow", "object_flow"}:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-activity-relation",
                        "Activity relationships must be control or object flows",
                        subject=relation.id,
                    )
                )
            if relation.type == "object_flow" and "object" not in {elements[relation.source].type, elements[relation.target].type}:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-object-flow",
                        "Object flow must connect an Object Node",
                        subject=relation.id,
                    )
                )
            if relation.type == "control_flow" and elements[relation.source].type == "decision" and not relation.name:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "unlabeled-decision",
                        "Decision branches require guard labels",
                        subject=relation.id,
                    )
                )
        if len(initial) == 1:
            start = initial[0]
            incoming_count = {item: 0 for item in view.include}
            outgoing_count = {item: 0 for item in view.include}
            for relation in relations:
                outgoing_count[relation.source] += 1
                incoming_count[relation.target] += 1
            if incoming_count[start]:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "activity-initial-incoming",
                        "Activity initial cannot have incoming flow",
                    )
                )
            for item in view.include:
                item_type = elements[item].type
                if item_type == "final" and outgoing_count[item]:
                    diagnostics.append(
                        Diagnostic(
                            "Q3",
                            "activity-final-outgoing",
                            "Activity final cannot have outgoing flow",
                            subject=item,
                        )
                    )
                if item_type in {"decision", "fork"} and outgoing_count[item] < 2:
                    diagnostics.append(
                        Diagnostic(
                            "Q3",
                            "activity-split-degree",
                            "Decision/fork requires at least two outgoing flows",
                            subject=item,
                        )
                    )
                if item_type in {"join", "merge"} and incoming_count[item] < 2:
                    diagnostics.append(
                        Diagnostic(
                            "Q3",
                            "activity-merge-degree" if item_type == "merge" else "activity-join-degree",
                            "Merge requires at least two incoming flows" if item_type == "merge" else "Join requires at least two incoming flows",
                            subject=item,
                        )
                    )
            reachable = {start}
            changed = True
            while changed:
                changed = False
                for relation in relations:
                    if relation.source in reachable and relation.target not in reachable:
                        reachable.add(relation.target)
                        changed = True
            for item in set(view.include) - reachable:
                if elements[item].type == "note" or (elements[item].type == "object" and elements[item].metadata.get("externalInput")):
                    continue
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "unreachable-activity-node",
                        "Activity node is unreachable",
                        subject=item,
                    )
                )
    if view.diagram_type == "component":
        for relation in relations:
            source_type = elements[relation.source].type
            target_type = elements[relation.target].type
            if relation.type == "connector" and {
                source_type,
                target_type,
            } != {"provided_interface", "required_interface"}:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-interface-connector",
                        "A connector joins one provided and one required interface",
                        subject=relation.id,
                    )
                )
            if relation.type == "dependency" and not (
                source_type == "component" and target_type == "component"
            ):
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-component-dependency",
                        "Component dependencies join components",
                        subject=relation.id,
                    )
                )
            if relation.type == "realization" and not (
                source_type == "component" and target_type == "provided_interface"
            ):
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-interface-realization",
                        "Realization runs from component to provided interface",
                        subject=relation.id,
                    )
                )
    if view.diagram_type == "deployment":
        for item in view.include:
            if elements[item].type != "deployment_node":
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-deployment-element",
                        "Deployment views select deployment nodes; artifacts are contained metadata",
                        subject=item,
                    )
                )
        for relation in relations:
            if relation.type != "communication_path":
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "invalid-deployment-relation",
                        "Deployment node relationships must be communication paths",
                        subject=relation.id,
                    )
                )
    if view.diagram_type == "package":
        course = load_yaml(ROOT / "governance" / "course-profile.yaml")
        allowed = set(
            load_yaml(ROOT / "governance" / "modeling-policy.yaml")["uml"]["package_relationships"]
        )
        if "package" not in course["required_diagram_types"]:
            diagnostics.append(Diagnostic("Q3", "course-profile", "Package is not required"))
        for relation in relations:
            if relation.type not in allowed:
                diagnostics.append(
                    Diagnostic(
                        "Q3",
                        "package-relation",
                        "Course profile permits package dependencies",
                        subject=relation.id,
                    )
                )
    return diagnostics
