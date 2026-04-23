from model import (
    Location,
    Portal,
    Wizard,
    Goblin,
    Crystal,
    WizardMoves,
    GoblinMoves,
    GameAction,
    GameState,
)
from agents import ReasoningWizard
from dataclasses import dataclass


class WizardGreedy(ReasoningWizard):
    def evaluation(self, state: GameState) -> float:
        # TODO YOUR CODE HERE
        wizard_locs = state.get_all_entity_locations(Wizard)

        # Wizard is dead 
        if not wizard_locs:
            return float('-inf')

        wizard_loc = wizard_locs[0]
        portal_locs = state.get_all_tile_locations(Portal)
        goblin_locs = state.get_all_entity_locations(Goblin)
        crystal_locs = state.get_all_entity_locations(Crystal)

        score = 0.0

        # Reward being close to the portal
        if portal_locs:
            portal = portal_locs[0]
            dist_to_portal = abs(wizard_loc.row - portal.row) + abs(wizard_loc.col - portal.col)
            score -= dist_to_portal * 2  # weighted heavily

        # Reward being close to crystals
        if crystal_locs:
            nearest_crystal_dist = min(
                abs(wizard_loc.row - c.row) + abs(wizard_loc.col - c.col)
                for c in crystal_locs
            )
            score -= nearest_crystal_dist

        # Reward collected crystals
        score += state.score * 10

        # Penalize being close to goblins
        for goblin_loc in goblin_locs:
            dist_to_goblin = abs(wizard_loc.row - goblin_loc.row) + abs(wizard_loc.col - goblin_loc.col)
            if dist_to_goblin == 0:
                return float('-inf')  # dead
            score += dist_to_goblin * 3  # stay far away

        return score


class WizardMiniMax(ReasoningWizard):
    max_depth: int = 2

    def evaluation(self, state: GameState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def is_terminal(self, state: GameState) -> bool:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        raise NotImplementedError


    def minimax(self, state: GameState, depth: int):
        # TODO YOUR CODE HERE
        raise NotImplementedError


class WizardAlphaBeta(ReasoningWizard):
    max_depth: int = 2

    def evaluation(self, state: GameState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def is_terminal(self, state: GameState) -> bool:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        raise NotImplementedError


    def alpha_beta_minimax(self, state: GameState, depth: int):
        # TODO YOUR CODE HERE
        raise NotImplementedError




class WizardExpectimax(ReasoningWizard):
    max_depth: int = 2

    def evaluation(self, state: GameState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def is_terminal(self, state: GameState) -> bool:
        # TODO YOUR CODE HERE
        raise NotImplementedError

    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        raise NotImplementedError


    def expectimax(self, state: GameState, depth: int):
        # TODO YOUR CODE HERE
        raise NotImplementedError
