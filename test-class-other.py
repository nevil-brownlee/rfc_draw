
import test_class_scope as tcs

print("tcs = %s (%s)" % (tcs, type(tcs)))
print("tcs.tcs_glob = %s (%s)" % (tcs.tcs_glob, type(tcs.tcs_glob)))
tcs_class = tcs.tcs_glob.test_class(5,6)
print("tcs_class %s" % tcs_class)
