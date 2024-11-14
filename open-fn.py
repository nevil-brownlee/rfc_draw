from tkinter.filedialog import askopenfilename

save_file_name = askopenfilename(
    title="Select .rdd file; cancel box if none")

# 'cancel' returns empty string

print("returned len %s" % len(save_file_name))
print("returned type %s" % type(save_file_name))

print("filename >%s<" % save_file_name)
