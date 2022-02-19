genrule(
    name = "rendered_black_entrypoint",
    srcs = [
        "entry_points.txt",
    ],
    outs = ["black_main.py"],
    cmd = "$TOOL --write=$OUT $SRC",
    tools = [
        "//tools/entrypoint_generator",
    ],
)

sh_cmd(
    name = "cmd_check_import_is_expanded",
    cmd = 'grep -q "from black import patched_main" $(location :rendered_black_entrypoint)',
    deps = [
        ":rendered_black_entrypoint",
    ],
)

sh_cmd(
    name = "cmd_check_command_is_expanded",
    cmd = 'grep -q "sys.exit(patched_main())" $(location :rendered_black_entrypoint)',
    deps = [
        ":rendered_black_entrypoint",
    ],
)

sh_test(
    name = "test_import_is_expanded",
    src = ":cmd_check_import_is_expanded",
    data = [
        ":rendered_black_entrypoint",
    ],
    deps = [
        ":cmd_check_import_is_expanded",
    ],
)

sh_test(
    name = "test_command_is_expanded",
    src = ":cmd_check_command_is_expanded",
    data = [
        ":rendered_black_entrypoint",
    ],
    deps = [
        ":cmd_check_command_is_expanded",
    ],
)
