import builtins
builtin_zip = builtins.zip


def zip(pipe1, name1, pipe2, name2, *, grouped=False):
    print("Building picamkit.ops.utils.zip")
    print(f"- name1: {name1}")
    print(f"- name2: {name2}")
    print(f"- grouped: {grouped}")
    
    def gen():
        for item1, item2 in builtin_zip(pipe1, pipe2):
            item1['name'] = name1
            item2['name'] = name2
        
            if grouped:
                items = [item1, item2]
                yield items
        
            else:
                yield item1
                yield item2

    return gen()

