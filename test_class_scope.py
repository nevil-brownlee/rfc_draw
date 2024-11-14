
class tcs_glob:

    def __init__(self):
        super().__init__()
        print("tcs_glob: __init__ called")
        
    def test_class(self, a, b):
        cl_obj_a = a;  cl_obj_b = b

        def cl_a_b(self):
            print("from cl_a_b: cl_obj_a %s, cl_obj_b %s" % (cl_obj_a, cl_obj_b))

class other:
    tg = tcs_glob()
    tt = tg.test_class(2, 3)
    print("tt >%s< (%s)" % (tt, type(tt)))

    print("tc_1.a >%s<, tc_a.b >%s<" % (tc_1.cl_obj_a, tc_1.cl_obj_b))
