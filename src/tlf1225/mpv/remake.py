from code import interact
from ctypes import cdll, c_void_p, c_char_p, c_int, c_int64, c_uint64, c_ulong, c_double, CFUNCTYPE, POINTER

mpv = cdll.LoadLibrary("D:/Python/libmpv/mpv-1.dll")
cp_vp = CFUNCTYPE(c_char_p, c_void_p)
cp_vp_cp = CFUNCTYPE(c_char_p, c_void_p, c_char_p)
vp = CFUNCTYPE(c_void_p)
ul = CFUNCTYPE(c_ulong)
cp_i = CFUNCTYPE(c_char_p, c_int)
i_vp = CFUNCTYPE(c_int, c_void_p)
i_vp_vp = CFUNCTYPE(c_int, c_void_p, c_void_p)
i_vp_i_i = CFUNCTYPE(c_int, c_void_p, c_int, c_int)
i_vp_ui64_cp_i = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_int)
i_vp_cp = CFUNCTYPE(c_int, c_void_p, c_char_p)
i_vp_ui64 = CFUNCTYPE(c_int, c_void_p, c_uint64)
i_vp_cpp = CFUNCTYPE(c_int, c_void_p, POINTER(c_char_p))
i_vp_cp_i_vp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_int, c_void_p)
i_vp_cp_cp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_char_p)
i_vp_vp_vp = CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p)
i_vp_vpp_vp = CFUNCTYPE(c_int, c_void_p, POINTER(c_void_p), c_void_p)
i_vp_ui64_cpp = CFUNCTYPE(c_int, c_void_p, c_uint64, POINTER(c_char_p))
i_vp_ui64_vp = CFUNCTYPE(c_int, c_void_p, c_uint64, c_void_p)
i_vp_cp_vp_vp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_void_p, c_void_p)
i_vp_ui64_cp_vp = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_void_p)
i_vp_ui64_cp_vp_vp = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_void_p, c_void_p)
i64_vp = CFUNCTYPE(c_int64, c_void_p)
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
cm_nd = cmd_p + ((1, "result"),)
ab_cm = con_tx + ((1, "reply_userdata"),)
cm_as = ab_cm + ((1, "args"),)

get_opt_p = con_tx + ((1, "name"),)
set_opt = get_opt = get_opt_p + ((1, "format"), (1, "data"))
set_opt_p = get_opt_p + dat
get_opt_a = con_tx + ((1, "reply_data"), (1, "name"), (1, "format"))
set_opt_a = get_opt_a + ((1, "data"),)

ob_opt = con_tx + ((1, "reply_data"), (1, "name"), (1, "format"))
unob_opt = con_tx + ((1, "registered_reply_userdata"),)

ev = (1, "event"),
en = (1, "dst"), (1, "src")
re = con_tx + ((1, "event"), (1, "enable"))
rl = con_tx + ((1, "min_level"),)
we = con_tx + ((1, "timeout"),)
swc = con_tx + ((1, "function"), (1, "d"))

hk = con_tx + ((1, "reply_userdata"), (1, "name"), (1, "priority"))
hk_c = con_tx + ((1, "id"),)

client_api_version = ul(("mpv_client_api_version", mpv), None)
error_string = cp_i(("mpv_error_string", mpv), err)
free = v_vp(("mpv_free", mpv), dat)

client_name = cp_vp(("mpv_client_name", mpv), con_tx)
client_id = i64_vp(("mpv_client_id", mpv), con_tx)

create = vp(("mpv_create", mpv), None)
initialize = i_vp(("mpv_initialize", mpv), con_tx)
destroy = v_vp(("mpv_destroy", mpv), con_tx)
terminate_destroy = v_vp(("mpv_terminate_destroy", mpv), con_tx)

create_client = vp_vp_cp(("mpv_create_client", mpv), cre_cli_p)
create_weak_client = vp_vp_cp(("mpv_create_weak_client", mpv), cre_cli_p)

load_config_file = i_vp_cp(("mpv_load_config_file", mpv), ld_conf_p)
get_time_us = i64_vp(("mpv_get_time_us", mpv), con_tx)
free_node_contents = v_vp(("mpv_free_node_contents", mpv), nd)

set_option = i_vp_cp_i_vp(("mpv_set_option", mpv), so)
set_option_string = i_vp_cp_cp(("mpv_set_option_string", mpv), set_opt_p)

command = i_vp_cpp(("mpv_command", mpv), cmd_p)
command_node = i_vp_vp_vp(("mpv_command_node", mpv), cm_nd)
command_ret = i_vp_vpp_vp(("mpv_command_ret", mpv), cm_nd)
command_string = i_vp_cp(("mpv_command_string", mpv), cmd_p)
command_async = i_vp_ui64_cpp(("mpv_command_async", mpv), cm_as)
command_node_async = i_vp_ui64_vp(("mpv_command_node_async", mpv), cm_as)
abort_async_command = v_vp_ui64(("mpv_abort_async_command", mpv), ab_cm)

set_property = i_vp_cp_vp_vp(("mpv_set_property", mpv), set_opt)
set_property_string = i_vp_cp_cp(("mpv_set_property_string", mpv), set_opt_p)
set_property_async = i_vp_ui64_cp_vp_vp(("mpv_set_property_async", mpv), set_opt_a)
get_property = i_vp_cp_vp_vp(("mpv_get_property", mpv), get_opt)
get_property_string = cp_vp_cp(("mpv_get_property_string", mpv), get_opt_p)
get_property_osd_string = cp_vp_cp(("mpv_get_property_osd_string", mpv), get_opt_p)
get_property_async = i_vp_ui64_cp_vp(("mpv_get_property_async", mpv), get_opt_a)
observe_property = i_vp_ui64_cp_vp(("mpv_observe_property", mpv), ob_opt)
unobserve_property = i_vp_ui64(("mpv_unobserve_property", mpv), unob_opt)
event_name = cp_i(("mpv_event_name", mpv), ev)
event_to_node = i_vp_vp(("mpv_event_to_node", mpv), en)
request_event = i_vp_i_i(("mpv_request_event", mpv), re)
request_log_messages = i_vp_cp(("mpv_request_log_messages", mpv), rl)
wait_event = vp_vp_d(("mpv_wait_event", mpv), we)
wakeup = v_vp(("mpv_wakeup", mpv), con_tx)
set_wakeup_callback = v_vp_f_vp(("mpv_set_wakeup_callback", mpv), swc)
wait_async_requests = v_vp(("mpv_wait_async_requests", mpv), con_tx)
hook_add = i_vp_ui64_cp_i(("mpv_hook_add", mpv), hk)
hook_continue = i_vp_ui64(("mpv_hook_continue", mpv), hk_c)

__all__ = ["client_api_version", "error_string", "free", "client_name", "client_id", "create", "initialize", "destroy", "terminate_destroy",
           "create_client", "create_weak_client", "load_config_file", "get_time_us", "free_node_contents", "set_option", "set_option_string",
           "command", "command_node", "command_ret", "command_string", "command_async", "command_node_async", "abort_async_command", "set_property",
           "set_property_string", "set_property_async", "get_property", "get_property_string", "get_property_osd_string", "get_property_async",
           "observe_property", "unobserve_property", "event_name", "event_to_node", "request_event", "request_log_messages", "wait_event", "wakeup",
           "set_wakeup_callback", "wait_async_requests", "hook_add", "hook_continue"]

if __name__ == '__main__':
    mpv_handle = create()
    initialize(mpv_handle)

    # set_option_string(mpv_handle, c_char_p(b"audio-display"), c_char_p(b"yes"))

    # mpv_client_handle = create_client(mpv_handle, c_char_p(b"Worker"))

    # client_name = client_name(mpv_client_handle)
    # client_id = client_id(mpv_client_handle)

    client_name = client_name(mpv_handle)
    client_id = client_id(mpv_handle)

    print(client_name)
    print(client_id)

    # noinspection SpellCheckingInspection
    command(mpv_handle, (c_char_p * 2)(c_char_p(b"loadfile"), c_char_p(b"ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr")))

    interact(banner="Mpv Player", local=locals(), exitmsg="Exit")

    command(mpv_handle, (c_char_p * 1)(c_char_p(b"quit")))

    # destroy(mpv_handle)

    terminate_destroy(mpv_handle)

    # free(mpv_handle)
