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
        wizard_locs = state.get_all_entity_locations(Wizard)

        # Wizard is dead
        if not wizard_locs:
            return float('-inf')

        wizard_loc = wizard_locs[0]
        portal_locs = state.get_all_tile_locations(Portal)
        goblin_locs = state.get_all_entity_locations(Goblin)
        crystal_locs = state.get_all_entity_locations(Crystal)

        score = 0.0

        # Reward being close to portal
        if portal_locs:
            portal = portal_locs[0]
            dist_to_portal = abs(wizard_loc.row - portal.row) + abs(wizard_loc.col - portal.col)
            score -= dist_to_portal * 2

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
            score += dist_to_goblin * 3

        return score

    def is_terminal(self, state: GameState) -> bool:
        # TODO YOUR CODE HERE
        wizard_locs = state.get_all_entity_locations(Wizard)
        if not wizard_locs:
            return True
        portal_locs = state.get_all_tile_locations(Portal)
        if portal_locs:
            portal = portal_locs[0]
            return wizard_locs[0] == portal
        return False

    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        best_action = None
        best_value = float('-inf')

        for action, result in self.get_successors(state):
            # Only consider wizard moves at the top level
            if not isinstance(action, WizardMoves):
                continue
            value = self.minimax(result, depth=1)
            if value > best_value:
                best_value = value
                best_action = action

        return best_action if best_action is not None else WizardMoves.STAY

    def minimax(self, state: GameState, depth: int):
        # TODO YOUR CODE HERE
        if self.is_terminal(state):
            return self.evaluation(state)

        active_entity = state.get_active_entity()

        # If it's the wizard's turn, this is a max node — increment depth
        if isinstance(active_entity, Wizard):
            if depth >= self.max_depth:
                return self.evaluation(state)
            best = float('-inf')
            for action, result in self.get_successors(state):
                best = max(best, self.minimax(result, depth + 1))
            return best

        # If it's a goblin's turn, this is a min node — don't increment depth
        else:
            worst = float('inf')
            for action, result in self.get_successors(state):
                worst = min(worst, self.minimax(result, depth))
            return worst


class WizardAlphaBeta(ReasoningWizard):
    max_depth: int = 2

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

        # Reward being close to portal
        if portal_locs:
            portal = portal_locs[0]
            dist_to_portal = abs(wizard_loc.row - portal.row) + abs(wizard_loc.col - portal.col)
            score -= dist_to_portal * 2

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
            score += dist_to_goblin * 3

        return score

    def is_terminal(self, state: GameState) -> bool:
        # TODO YOUR CODE HERE
        wizard_locs = state.get_all_entity_locations(Wizard)
        if not wizard_locs:
            return True
        portal_locs = state.get_all_tile_locations(Portal)
        if portal_locs:
            portal = portal_locs[0]
            return wizard_locs[0] == portal
        return False


    def react(self, state: GameState) -> WizardMoves:
        # TODO YOUR CODE HERE
        best_action = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for action, result in self.get_successors(state):
            if not isinstance(action, WizardMoves):
                continue
            value = self.alpha_beta_minimax(result, depth=1, alpha=alpha, beta=beta)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)

        return best_action if best_action is not None else WizardMoves.STAY


    def alpha_beta_minimax(self, state: GameState, depth: int, alpha: float, beta: float) -> float:
        # TODO YOUR CODE HERE
        if self.is_terminal(state):
            return self.evaluation(state)

        active_entity = state.get_active_entity()

        # Max node
        if isinstance(active_entity, Wizard):
            if depth >= self.max_depth:
                return self.evaluation(state)
            best = float('-inf')
            for action, result in self.get_successors(state):
                best = max(best, self.alpha_beta_minimax(result, depth + 1, alpha, beta))
                alpha = max(alpha, best)
                if beta <= alpha:
                    break  # beta cutoff
            return best

        # Min node
        else:
            worst = float('inf')
            for action, result in self.get_successors(state):
                worst = min(worst, self.alpha_beta_minimax(result, depth, alpha, beta))
                beta = min(beta, worst)
                if beta <= alpha:
                    break  # alpha cutoff
            return worst




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
