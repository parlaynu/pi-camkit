
def chain(pipe1, name1, pipe2, name2):
    print("Building picamkit.ops.utils.chain")
    print(f"- name1: {name1}")
    print(f"- name2: {name2}")
    
    def gen():
        for item in pipe1:
            item['name'] = name1
            yield item
        for item in pipe2:
            item['name'] = name2
            yield item

    return gen()



