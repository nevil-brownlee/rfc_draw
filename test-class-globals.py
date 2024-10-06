
class draw_headers:
    headers = []

class c_a:
    def __init__(self):
        draw_headers.headers.append("c_a 1")

    def p(self):
        print("from c_a: h %s" % h.headers)


x = c_a()
print("h >%s<" % draw_headers.headers)

