from typing import Any

# Credits to https://code.activestate.com/recipes/215912-union-find-data-structure/


class UnionFind:
    def __init__(self) -> None:
        self.weights: dict[int, int] = {}
        self.pointers: dict[int, int] = {}
        self.indexes_to_objects: dict[int, Any] = {}
        self.objects_to_indexes: dict[Any, int] = {}

    def insert_objects(self, objects: Any) -> None:
        for object in objects:
            self.find(object)

    def build_if_not_exists(self, object: Any) -> Any:
        new_index = len(self.objects_to_indexes)

        self.weights[new_index] = 1
        self.objects_to_indexes[object] = new_index
        self.indexes_to_objects[new_index] = object
        self.pointers[new_index] = new_index

        return object

    def find(self, object: Any) -> Any:
        if object not in self.objects_to_indexes:
            return self.build_if_not_exists(object)

        object_indexes = [self.objects_to_indexes[object]]
        object_pointers = self.pointers[object_indexes[-1]]

        while object_pointers != object_indexes[-1]:
            object_indexes.append(object_pointers)
            object_pointers = self.pointers[object_pointers]

        for index in object_indexes:
            self.pointers[index] = object_pointers

        return self.indexes_to_objects[object_pointers]

    def union(self, object_a: Any, object_b: Any) -> None:
        object_a_set = self.find(object_a)
        object_b_set = self.find(object_b)

        if object_a_set != object_b_set:
            object_a_indexes = self.objects_to_indexes[object_a_set]
            object_b_indexes = self.objects_to_indexes[object_b_set]
            object_a_weights = self.weights[object_a_indexes]
            object_b_weights = self.weights[object_b_indexes]

            if object_a_weights < object_b_weights:
                (
                    object_a_set,
                    object_b_set,
                    object_a_indexes,
                    object_b_indexes,
                    object_a_weights,
                    object_b_weights,
                ) = (
                    object_b_set,
                    object_a_set,
                    object_b_indexes,
                    object_a_indexes,
                    object_b_weights,
                    object_a_weights,
                )

            self.weights[object_a_indexes] = object_a_weights + object_b_weights
            del self.weights[object_b_indexes]
            self.pointers[object_b_indexes] = object_a_indexes
