from __future__ import annotations
from typing import Any, Dict, Iterable, Mapping, Tuple


class FuzzySet:
    def __init__(self, memberships: Mapping[Any, float]) -> None:
        self.memberships: Dict[Any, float] = {}
        for element, value in memberships.items():
            membership = float(value)
            if not 0.0 <= membership <= 1.0:
                raise ValueError(f"Membership degree for {element!r} must be between 0 and 1.")
            self.memberships[element] = membership

    def membership(self, element: Any) -> float:
        return self.memberships.get(element, 0.0)

    def elements(self) -> set[Any]:
        return set(self.memberships.keys())

    def __repr__(self) -> str:
        sorted_items = sorted(self.memberships.items(), key=lambda item: repr(item[0]))
        return f"FuzzySet({{{', '.join(f'{repr(k)}: {v:.2f}' for k, v in sorted_items)}}})"

    def union(self, other: FuzzySet) -> FuzzySet:
        result: Dict[Any, float] = {}
        for element in self.elements() | other.elements():
            result[element] = max(self.membership(element), other.membership(element))
        return FuzzySet(result)

    def intersection(self, other: FuzzySet) -> FuzzySet:
        result: Dict[Any, float] = {}
        for element in self.elements() | other.elements():
            result[element] = min(self.membership(element), other.membership(element))
        return FuzzySet(result)

    def complement(self) -> FuzzySet:
        return FuzzySet({element: 1.0 - membership for element, membership in self.memberships.items()})

    def difference(self, other: FuzzySet) -> FuzzySet:
        result: Dict[Any, float] = {}
        for element in self.elements() | other.elements():
            result[element] = min(self.membership(element), 1.0 - other.membership(element))
        return FuzzySet(result)

    def cartesian_product(self, other: FuzzySet) -> "FuzzyRelation":
        relation: Dict[Tuple[Any, Any], float] = {}
        for x in self.elements():
            for y in other.elements():
                relation[(x, y)] = min(self.membership(x), other.membership(y))
        return FuzzyRelation(relation)


class FuzzyRelation:
    def __init__(self, memberships: Mapping[Tuple[Any, Any], float]) -> None:
        self.memberships: Dict[Tuple[Any, Any], float] = {}
        for pair, value in memberships.items():
            membership = float(value)
            if not 0.0 <= membership <= 1.0:
                raise ValueError(f"Membership degree for relation pair {pair!r} must be between 0 and 1.")
            self.memberships[pair] = membership

    def membership(self, pair: Tuple[Any, Any]) -> float:
        return self.memberships.get(pair, 0.0)

    def domain(self) -> set[Any]:
        return {pair[0] for pair in self.memberships}

    def codomain(self) -> set[Any]:
        return {pair[1] for pair in self.memberships}

    def __repr__(self) -> str:
        sorted_items = sorted(self.memberships.items(), key=lambda item: (repr(item[0][0]), repr(item[0][1])))
        return f"FuzzyRelation({{{', '.join(f'{repr(k)}: {v:.2f}' for k, v in sorted_items)}}})"

    def max_min_composition(self, other: FuzzyRelation) -> FuzzyRelation:
        result: Dict[Tuple[Any, Any], float] = {}
        self_domain = self.domain()
        self_codomain = self.codomain()
        other_codomain = other.codomain()
        inner_set = self_codomain | other.domain()

        for x in self_domain:
            for z in other_codomain:
                max_value = 0.0
                for y in inner_set:
                    left = self.membership((x, y))
                    right = other.membership((y, z))
                    current = min(left, right)
                    if current > max_value:
                        max_value = current
                if max_value > 0.0:
                    result[(x, z)] = max_value
        return FuzzyRelation(result)


if __name__ == "__main__":
    A = FuzzySet({"a": 0.2, "b": 0.8, "c": 0.4})
    B = FuzzySet({"b": 0.6, "c": 0.3, "d": 1.0})
    C = FuzzySet({"c": 0.9, "d": 0.4, "e": 0.7})

    print("Set A:", A)
    print("Set B:", B)
    print("A ∪ B:", A.union(B))
    print("A ∩ B:", A.intersection(B))
    print("A complement:", A.complement())
    print("A - B:", A.difference(B))

    R = A.cartesian_product(B)
    S = B.cartesian_product(C)
    print("Relation R (A × B):", R)
    print("Relation S (B × C):", S)
    print("Max-min composition R ∘ S:", R.max_min_composition(S))
