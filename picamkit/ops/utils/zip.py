from typing import Iterable, Generator
import builtins


def zip(
    pipe1: Iterable[dict],
    name1: str,
    pipe2: Iterable[dict],
    name2: str,
    *, 
    grouped: bool = False
) -> Generator[dict, None, None]:
    """Rejoin to branches of a pipeline that have been separated using the 'tee' operator.

    When 'grouped' is False, yield each input separatels. When True, group them together
    into a list an yield the list.
    """

    print("Building picamkit.ops.utils.zip")
    print(f"- name1: {name1}")
    print(f"- name2: {name2}")
    print(f"- grouped: {grouped}")
    
    def gen():
        for item1, item2 in builtins.zip(pipe1, pipe2):
            item1['name'] = name1
            item2['name'] = name2
        
            if grouped:
                items = [item1, item2]
                yield items
        
            else:
                yield item1
                yield item2

    return gen()

