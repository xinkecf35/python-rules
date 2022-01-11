subinclude("//build_defs:python")

python_binary(
    name = "entrypoint_generator",
    main = "create_entrypoints.py",
    resources = ["entry_point.tmpl"],
    visibility = ["PUBLIC"],
    zip_safe = False,
)