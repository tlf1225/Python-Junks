from ctypes import CDLL, c_void_p, c_char_p, c_int, c_int64, c_uint64, c_ulong, c_double, CFUNCTYPE, POINTER
from ctypes.util import find_library

mpv = CDLL(find_library("mpv-1.dll"))

cp_i = CFUNCTYPE(c_char_p, c_int)
cp_vp = CFUNCTYPE(c_char_p, c_void_p)
cp_vp_cp = CFUNCTYPE(c_char_p, c_void_p, c_char_p)
i_vp = CFUNCTYPE(c_int, c_void_p)
i_vp_vp = CFUNCTYPE(c_int, c_void_p, c_void_p)
i_vp_cp = CFUNCTYPE(c_int, c_void_p, c_char_p)
i_vp_cp_cp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_char_p)
i_vp_cp_vp_vp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_void_p, c_void_p)
i_vp_cp_i_vp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_int, c_void_p)
i_vp_cpp = CFUNCTYPE(c_int, c_void_p, POINTER(c_char_p))
i_vp_i_i = CFUNCTYPE(c_int, c_void_p, c_int, c_int)
i_vp_ui64 = CFUNCTYPE(c_int, c_void_p, c_uint64)
i_vp_ui64_cp_i = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_int)
i_vp_vp_vp = CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p)
i_vp_vpp_vp = CFUNCTYPE(c_int, c_void_p, POINTER(c_void_p), c_void_p)
i_vp_ui64_cpp = CFUNCTYPE(c_int, c_void_p, c_uint64, POINTER(c_char_p))
i_vp_ui64_vp = CFUNCTYPE(c_int, c_void_p, c_uint64, c_void_p)
i_vp_ui64_cp_vp = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_void_p)
i_vp_ui64_cp_vp_vp = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_void_p, c_void_p)
i_vpp_vp_vp = CFUNCTYPE(c_int, POINTER(c_void_p), c_void_p, c_void_p)
i64_vp = CFUNCTYPE(c_int64, c_void_p)
ul = CFUNCTYPE(c_ulong)
ui64_vp = CFUNCTYPE(c_int64, c_void_p)
vp = CFUNCTYPE(c_void_p)
vp_vp = CFUNCTYPE(c_void_p, c_void_p)
v_vp = CFUNCTYPE(None, c_void_p)
v_vp_ui64 = CFUNCTYPE(None, c_void_p, c_uint64)
v_vp_f_vp = CFUNCTYPE(None, c_void_p, v_vp, c_void_p)
vp_vp_cp = CFUNCTYPE(c_void_p, c_void_p, c_char_p)
vp_vp_d = CFUNCTYPE(c_void_p, c_void_p, c_double)

con_tx = (1, "ctx"),
err = (1, "error"),
dat = (1, "data"),

cre_cli_p = con_tx + ((1, "name"),)
ld_conf_p = con_tx + ((1, "filename"),)

nd = (1, "node"),
so = cre_cli_p + ((1, "format"),) + dat
cmd_p = con_tx + ((1, "args"),)
cm_nd = cmd_p + ((2, "result", POINTER(c_char_p)),)
ab_cm = con_tx + ((1, "reply_userdata"),)
cm_as = ab_cm + ((1, "args"),)

get_opt_p = con_tx + ((1, "name"),)
set_opt = get_opt = get_opt_p + ((1, "format"), (1, "data"))
set_opt_p = get_opt_p + dat
get_opt_a = con_tx + ((1, "reply_data"), (1, "name"), (1, "format"))
set_opt_a = get_opt_a + ((1, "data"),)

ob_opt = con_tx + ((1, "reply_data"), (1, "name"), (1, "format"))
u_ob_opt = con_tx + ((1, "registered_reply_userdata"),)

ev = (1, "event"),
en = (1, "dst"), (1, "src")
re = con_tx + ((1, "event"), (1, "enable"))
rl = con_tx + ((1, "min_level"),)
we = con_tx + ((1, "timeout"),)
swc = con_tx + ((1, "function"), (1, "d"))

hk = con_tx + ((1, "reply_userdata"), (1, "name"), (1, "priority"))
hk_c = con_tx + ((1, "id"),)

ctc = (2, "res"), (1, "mpv"), (1, "params")
cts = (1, "ctx"), (1, "param")
csc = (1, "ctx"), (1, "callback"), (1, "callback_ctx")

# noinspection PyArgumentList
client_api_version = ul(("mpv_client_api_version", mpv), None)
# noinspection PyArgumentList
error_string = cp_i(("mpv_error_string", mpv), err)
# noinspection PyArgumentList
free = v_vp(("mpv_free", mpv), dat)

# noinspection PyArgumentList
client_name = cp_vp(("mpv_client_name", mpv), con_tx)
# noinspection PyArgumentList
client_id = i64_vp(("mpv_client_id", mpv), con_tx)

# noinspection PyArgumentList
create = vp(("mpv_create", mpv), None)
# noinspection PyArgumentList
initialize = i_vp(("mpv_initialize", mpv), con_tx)
# noinspection PyArgumentList
destroy = v_vp(("mpv_destroy", mpv), con_tx)
# noinspection PyArgumentList
terminate_destroy = v_vp(("mpv_terminate_destroy", mpv), con_tx)

# noinspection PyArgumentList
create_client = vp_vp_cp(("mpv_create_client", mpv), cre_cli_p)
# noinspection PyArgumentList
create_weak_client = vp_vp_cp(("mpv_create_weak_client", mpv), cre_cli_p)
# noinspection PyArgumentList
load_config_file = i_vp_cp(("mpv_load_config_file", mpv), ld_conf_p)
# noinspection PyArgumentList
get_time_us = i64_vp(("mpv_get_time_us", mpv), con_tx)
# noinspection PyArgumentList
free_node_contents = v_vp(("mpv_free_node_contents", mpv), nd)

# noinspection PyArgumentList
set_option = i_vp_cp_i_vp(("mpv_set_option", mpv), so)
# noinspection PyArgumentList
set_option_string = i_vp_cp_cp(("mpv_set_option_string", mpv), set_opt_p)

# noinspection PyArgumentList
command = i_vp_cpp(("mpv_command", mpv), cmd_p)
# noinspection PyArgumentList
command_node = i_vp_vp_vp(("mpv_command_node", mpv), cm_nd)
# noinspection PyArgumentList
command_ret = i_vp_vpp_vp(("mpv_command_ret", mpv), cm_nd)
# noinspection PyArgumentList
command_string = i_vp_cp(("mpv_command_string", mpv), cmd_p)
# noinspection PyArgumentList
command_async = i_vp_ui64_cpp(("mpv_command_async", mpv), cm_as)
# noinspection PyArgumentList
command_node_async = i_vp_ui64_vp(("mpv_command_node_async", mpv), cm_as)
# noinspection PyArgumentList
abort_async_command = v_vp_ui64(("mpv_abort_async_command", mpv), ab_cm)

# noinspection PyArgumentList
set_property = i_vp_cp_vp_vp(("mpv_set_property", mpv), set_opt)
# noinspection PyArgumentList
set_property_string = i_vp_cp_cp(("mpv_set_property_string", mpv), set_opt_p)
# noinspection PyArgumentList
set_property_async = i_vp_ui64_cp_vp_vp(("mpv_set_property_async", mpv), set_opt_a)
# noinspection PyArgumentList
get_property = i_vp_cp_vp_vp(("mpv_get_property", mpv), get_opt)
# noinspection PyArgumentList
get_property_string = cp_vp_cp(("mpv_get_property_string", mpv), get_opt_p)
# noinspection PyArgumentList
get_property_osd_string = cp_vp_cp(("mpv_get_property_osd_string", mpv), get_opt_p)
# noinspection PyArgumentList
get_property_async = i_vp_ui64_cp_vp(("mpv_get_property_async", mpv), get_opt_a)
# noinspection PyArgumentList
observe_property = i_vp_ui64_cp_vp(("mpv_observe_property", mpv), ob_opt)
# noinspection PyArgumentList, SpellCheckingInspection
unobserve_property = i_vp_ui64(("mpv_unobserve_property", mpv), u_ob_opt)

# noinspection PyArgumentList
event_name = cp_i(("mpv_event_name", mpv), ev)
# noinspection PyArgumentList
event_to_node = i_vp_vp(("mpv_event_to_node", mpv), en)
# noinspection PyArgumentList
request_event = i_vp_i_i(("mpv_request_event", mpv), re)
# noinspection PyArgumentList
request_log_messages = i_vp_cp(("mpv_request_log_messages", mpv), rl)
# noinspection PyArgumentList
wait_event = vp_vp_d(("mpv_wait_event", mpv), we)
# noinspection PyArgumentList
wakeup = v_vp(("mpv_wakeup", mpv), con_tx)
# noinspection PyArgumentList
set_wakeup_callback = v_vp_f_vp(("mpv_set_wakeup_callback", mpv), swc)
# noinspection PyArgumentList
wait_async_requests = v_vp(("mpv_wait_async_requests", mpv), con_tx)

# noinspection PyArgumentList
hook_add = i_vp_ui64_cp_i(("mpv_hook_add", mpv), hk)
# noinspection PyArgumentList
hook_continue = i_vp_ui64(("mpv_hook_continue", mpv), hk_c)

# noinspection PyArgumentList
render_context_create = i_vpp_vp_vp(("mpv_render_context_create", mpv), ctc)
# noinspection PyArgumentList
render_context_set_parameter = i_vp_vp(("mpv_render_context_set_parameter", mpv), cts)
# noinspection PyArgumentList
render_context_get_info = i_vp_vp(("mpv_render_context_get_info", mpv), cts)
# noinspection PyArgumentList
render_context_set_update_callback = v_vp_f_vp(("mpv_render_context_set_update_callback", mpv), csc)
# noinspection PyArgumentList
render_context_update = ui64_vp(("mpv_render_context_update", mpv), con_tx)
# noinspection PyArgumentList
render_context_render = i_vp_vp(("mpv_render_context_render", mpv), cts)
# noinspection PyArgumentList
render_context_report_swap = v_vp(("mpv_render_context_report_swap", mpv), con_tx)
# noinspection PyArgumentList
render_context_free = v_vp(("mpv_render_context_free", mpv), con_tx)

# noinspection SpellCheckingInspection
__all__ = ["client_api_version", "error_string", "free", "client_name", "client_id", "create", "initialize", "destroy", "terminate_destroy",
           "create_client", "create_weak_client", "load_config_file", "get_time_us", "free_node_contents", "set_option", "set_option_string",
           "command", "command_node", "command_ret", "command_string", "command_async", "command_node_async", "abort_async_command", "set_property",
           "set_property_string", "set_property_async", "get_property", "get_property_string", "get_property_osd_string", "get_property_async",
           "observe_property", "unobserve_property", "event_name", "event_to_node", "request_event", "request_log_messages", "wait_event", "wakeup",
           "set_wakeup_callback", "wait_async_requests", "hook_add", "hook_continue", "render_context_create", "render_context_set_parameter",
           "render_context_set_update_callback", "render_context_update", "render_context_render", "render_context_report_swap",
           "render_context_free"]
