from model import (
    Location,
    Portal,
    EmptyEntity,
    Wizard,
    Goblin,
    Crystal,
    WizardMoves,
    GoblinMoves,
    GameAction,
    GameState,
)
from agents import WizardSearchAgent
import heapq
from dataclasses import dataclass
from collections import deque


class WizardDFS(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, list[WizardMoves]] = {}
    search_stack: list[SearchState] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = []
        self.search_stack = [initial_search_state]
        self.visited = set()

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def next_search_expansion(self) -> GameState | None:
        # TODO: YOUR CODE HERE
        while self.search_stack:
            state = self.search_stack.pop()
            if state in self.visited:
                continue
            self.visited.add(state)
            if self.is_goal(state):
                self.plan = list(reversed(self.paths[state]))
                return None
            return self.search_to_game(state)
        return None

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        # TODO: YOUR CODE HERE
        source_search = self.game_to_search(source)
        target_search = self.game_to_search(target)

        # Only visit states we haven't seen before
        if target_search not in self.paths:
            self.paths[target_search] = self.paths[source_search] + [action]
            self.search_stack.append(target_search)


class WizardBFS(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, list[WizardMoves]] = {}
    search_stack: list[SearchState] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = []
        self.search_queue = deque([initial_search_state])

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def next_search_expansion(self) -> GameState | None:
        # TODO: YOUR CODE HERE
        while self.search_queue:
            state = self.search_queue.popleft() # difference from DFS
            if self.is_goal(state):
                self.plan = list(reversed(self.paths[state]))
                return None
            return self.search_to_game(state)
        return None

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        # TODO: YOUR CODE HERE
        source_search = self.game_to_search(source)
        target_search = self.game_to_search(target)

        if target_search not in self.paths:
            self.paths[target_search] = self.paths[source_search] + [action]
            self.search_queue.append(target_search)

class WizardUCS(WizardBFS):
    pass


class WizardAstar(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, tuple[float, list[WizardMoves]]] = {}
    search_pq: list[tuple[float, SearchState]] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = 0, []
        self.search_pq = [(0, initial_search_state)]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def cost(self, source: GameState, target: GameState, action: WizardMoves) -> float:
        return 1

    def heuristic(self, target: GameState) -> float:
        # TODO: YOUR CODE HERE
        search_state = self.game_to_search(target)
        wizard = search_state.wizard_loc
        portal = search_state.portal_loc
        return abs(wizard.row - portal.row) + abs(wizard.col - portal.col)

    def next_search_expansion(self) -> GameState | None:
        # TODO: YOUR CODE HERE
        while self.search_pq:
            f_score, state = heapq.heappop(self.search_pq)
            # skip if we already found a better path to this state
            if state not in self.paths:
                continue
            best_cost, _ = self.paths[state]
            if f_score > best_cost + self.heuristic(self.search_to_game(state)):
                continue
            if self.is_goal(state):
                self.plan = list(reversed(self.paths[state][1]))
                return None
            return self.search_to_game(state)
        return None

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        # TODO: YOUR CODE HERE
        source_search = self.game_to_search(source)
        target_search = self.game_to_search(target)

        source_cost, _ = self.paths[source_search]
        new_cost = source_cost + self.cost(source, target, action)

        if target_search not in self.paths or new_cost < self.paths[target_search][0]:
            self.paths[target_search] = (new_cost, self.paths[source_search][1] + [action])
            f_score = new_cost + self.heuristic(target)
            heapq.heappush(self.search_pq, (f_score, target_search))


class CrystalSearchWizard(WizardSearchAgent):
    # TODO: YOUR CODE HERE

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def next_search_expansion(self) -> GameState | None:
        # TODO YOUR CODE HEREs
        raise NotImplementedError

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        # TODO YOUR CODE HERE
        raise NotImplementedError



class SuboptimalCrystalSearchWizard(CrystalSearchWizard):

    def heuristic(self, target: SearchState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError
