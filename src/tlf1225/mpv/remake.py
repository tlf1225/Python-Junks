from ctypes import CDLL, c_void_p, c_char_p, c_int, c_int64, c_uint64, c_ulong, c_double, CFUNCTYPE, POINTER, Structure, Union, c_size_t
from ctypes.util import find_library

mpv = CDLL(find_library("mpv-1.dll"))

MPVError = {
    0: "MPV_ERROR_SUCCESS",
    -1: "MPV_ERROR_EVENT_QUEUE_FULL",
    -2: "MPV_ERROR_NOMEM",
    -3: "MPV_ERROR_UNINITIALIZED",
    -4: "MPV_ERROR_INVALID_PARAMETER",
    -5: "MPV_ERROR_OPTION_NOT_FOUND",
    -6: "MPV_ERROR_OPTION_FORMAT",
    -7: "MPV_ERROR_OPTION_ERROR",
    -8: "MPV_ERROR_PROPERTY_NOT_FOUND",
    -9: "MPV_ERROR_PROPERTY_FORMAT",
    -10: "MPV_ERROR_PROPERTY_UNAVAILABLE",
    -11: "MPV_ERROR_PROPERTY_ERROR",
    -12: "MPV_ERROR_COMMAND",
    -13: "MPV_ERROR_LOADING_FAILED",
    -14: "MPV_ERROR_AO_INIT_FAILED",
    -15: "MPV_ERROR_VO_INIT_FAILED",
    -16: "MPV_ERROR_NOTHING_TO_PLAY",
    -17: "MPV_ERROR_UNKNOWN_FORMAT",
    -18: "MPV_ERROR_UNSUPPORTED",
    -19: "MPV_ERROR_NOT_IMPLEMENTED",
    -20: "MPV_ERROR_GENERIC"
}

MPVFormat = {
    0: "MPV_FORMAT_NONE",
    1: "MPV_FORMAT_STRING",
    2: "MPV_FORMAT_OSD_STRING",
    3: "MPV_FORMAT_FLAG",
    4: "MPV_FORMAT_INT64",
    5: "MPV_FORMAT_DOUBLE",
    6: "MPV_FORMAT_NODE",
    7: "MPV_FORMAT_NODE_ARRAY",
    8: "MPV_FORMAT_NODE_MAP",
    9: "MPV_FORMAT_BYTE_ARRAY"
}

MPVEventId = {
    0: "MPV_EVENT_NONE",
    1: "MPV_EVENT_SHUTDOWN",
    2: "MPV_EVENT_LOG_MESSAGE",
    3: "MPV_EVENT_GET_PROPERTY_REPLY",
    4: "MPV_EVENT_SET_PROPERTY_REPLY",
    5: "MPV_EVENT_COMMAND_REPLY",
    6: "MPV_EVENT_START_FILE",
    7: "MPV_EVENT_END_FILE",
    8: "MPV_EVENT_FILE_LOADED",
    # 9: "MPV_EVENT_TRACKS_CHANGED",
    # 10: "MPV_EVENT_TRACK_SWITCHED",
    # 11: "MPV_EVENT_IDLE",
    # 12: "MPV_EVENT_PAUSE",
    # 13: "MPV_EVENT_UNPAUSE",
    # 14: "MPV_EVENT_TICK",
    # 15: "MPV_EVENT_SCRIPT_INPUT_DISPATCH",
    16: "MPV_EVENT_CLIENT_MESSAGE",
    17: "MPV_EVENT_VIDEO_RECONFIG",
    18: "MPV_EVENT_AUDIO_RECONFIG",
    # 19: "MPV_EVENT_METADATA_UPDATE",
    20: "MPV_EVENT_SEEK",
    21: "MPV_EVENT_PLAYBACK_RESTART",
    22: "MPV_EVENT_PROPERTY_CHANGE",
    # 23: "MPV_EVENT_CHAPTER_CHANGE",
    24: "MPV_EVENT_QUEUE_OVERFLOW",
    25: "MPV_EVENT_HOOK"
}

MPVLog = {
    0: "MPV_LOG_LEVEL_NONE",
    10: "MPV_LOG_LEVEL_FATAL",
    20: "MPV_LOG_LEVEL_ERROR",
    30: "MPV_LOG_LEVEL_WARN",
    40: "MPV_LOG_LEVEL_INFO",
    50: "MPV_LOG_LEVEL_V",
    60: "MPV_LOG_LEVEL_DEBUG",
    70: "MPV_LOG_LEVEL_TRACE"
}

MPVEndFileReason = {
    0: "MPV_END_FILE_REASON_EOF",
    2: "MPV_END_FILE_REASON_STOP",
    3: "MPV_END_FILE_REASON_QUIT",
    4: "MPV_END_FILE_REASON_ERROR",
    5: "MPV_END_FILE_REASON_REDIRECT"
}

MPVRenderParamType = {
    0: "MPV_RENDER_PARAM_INVALID",
    1: "MPV_RENDER_PARAM_API_TYPE",
    2: "MPV_RENDER_PARAM_OPENGL_INIT_PARAMS",
    3: "MPV_RENDER_PARAM_OPENGL_FBO",
    4: "MPV_RENDER_PARAM_FLIP_Y",
    5: "MPV_RENDER_PARAM_DEPTH",
    6: "MPV_RENDER_PARAM_ICC_PROFILE",
    7: "MPV_RENDER_PARAM_AMBIENT_LIGHT",
    8: "MPV_RENDER_PARAM_X11_DISPLAY",
    9: "MPV_RENDER_PARAM_WL_DISPLAY",
    10: "MPV_RENDER_PARAM_ADVANCED_CONTROL",
    11: "MPV_RENDER_PARAM_NEXT_FRAME_INFO",
    12: "MPV_RENDER_PARAM_BLOCK_FOR_TARGET_TIME",
    13: "MPV_RENDER_PARAM_SKIP_RENDERING",
    14: "MPV_RENDER_PARAM_DRM_DISPLAY",
    15: "MPV_RENDER_PARAM_DRM_DRAW_SURFACE_SIZE",
    16: "MPV_RENDER_PARAM_DRM_DISPLAY_V2",
    17: "MPV_RENDER_PARAM_SW_SIZE",
    18: "MPV_RENDER_PARAM_SW_FORMAT",
    19: "MPV_RENDER_PARAM_SW_STRIDE",
    20: "MPV_RENDER_PARAM_SW_POINTER"
}

MPVRenderFrameInfoFlags = {
    1: "MPV_RENDER_FRAME_INFO_PRESENT",
    2: "MPV_RENDER_FRAME_INFO_REDRAW",
    4: "MPV_RENDER_FRAME_INFO_REPEAT",
    8: "MPV_RENDER_FRAME_INFO_BLOCK_VSYNC"
}

MPVRenderUpdateFlag = {
    1: "MPV_RENDER_UPDATE_FRAME"
}


class MPVEventStartFile(Structure):
    _fields_ = (
        ("playlist_entry_id", c_int64),
    )


class MPVEventEndFile(Structure):
    _fields_ = (
        ("reason", c_int),
        ("error", c_int),
        ("playlist_entry_id", c_int64),
        ("playlist_insert_id", c_int64),
        ("playlist_insert_num_entries", c_int64)
    )


class MPVEventClientMessage(Structure):
    _fields_ = (
        ("num_args", c_int),
        ("args", POINTER(c_char_p))
    )


class MPVEventHook(Structure):
    _fields_ = (
        ("name", c_char_p),
        ("id", c_uint64)
    )


class MPVEventLogMessage(Structure):
    _fields_ = (
        ("prefix", c_char_p),
        ("level", c_char_p),
        ("text", c_char_p),
        ("log_level", c_int)
    )


class MPVEventProperty(Structure):
    _fields_ = (
        ("name", c_char_p),
        ("format", c_int),
        ("data", c_void_p)
    )


class MPVEvent(Structure):
    _fields_ = (
        ("event_id", c_int),
        ("error", c_int),
        ("reply_userdata", c_uint64),
        ("data", c_void_p)
    )


class MPVByteArray(Structure):
    _fields_ = (
        ("data", c_void_p),
        ("size", c_size_t)
    )


class MPVNodeList(Structure):
    pass


class MPVUnion(Union):
    _fields_ = (
        ("string", c_char_p),
        ("flag", c_int),
        ("int64", c_int64),
        ("double", c_double),
        ("list", POINTER(MPVNodeList)),
        ("ba", POINTER(MPVByteArray))
    )


class MPVNode(Structure):
    _fields_ = (
        ("u", MPVUnion),
        ("mpv_format", c_int)
    )


MPVNodeList._fields_ = (
    ("num", c_int),
    ("values", POINTER(MPVNode)),
    ("keys", POINTER(c_char_p))
)


class MPVEventCommand(Structure):
    _fields_ = (
        ("result", MPVNode),
    )


class MPVRenderFrameInfo(Structure):
    _fields_ = (
        ("flags", c_uint64),
        ("target_time", c_int64)
    )


class MPVRenderParam(Structure):
    _fields_ = (
        ("type", c_int),
        ("data", c_void_p)
    )


cp_i = CFUNCTYPE(c_char_p, c_int)
cp_vp = CFUNCTYPE(c_char_p, c_void_p)
cp_vp_cp = CFUNCTYPE(c_char_p, c_void_p, c_char_p)
i_vp = CFUNCTYPE(c_int, c_void_p)
i_nd_ev = CFUNCTYPE(c_int, MPVNode, MPVEvent)
i_vp_cp = CFUNCTYPE(c_int, c_void_p, c_char_p)
i_vp_cp_cp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_char_p)
i_vp_cp_vp_vp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_void_p, c_void_p)
i_vp_cp_i_vp = CFUNCTYPE(c_int, c_void_p, c_char_p, c_int, c_void_p)
i_vp_cpp = CFUNCTYPE(c_int, c_void_p, POINTER(c_char_p))
i_vp_i_i = CFUNCTYPE(c_int, c_void_p, c_int, c_int)
i_vp_ui64 = CFUNCTYPE(c_int, c_void_p, c_uint64)
i_vp_ui64_cp_i = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_int)
i_vp_rp = CFUNCTYPE(c_int, c_void_p, MPVRenderParam)
i_vp_rpp = CFUNCTYPE(c_int, c_void_p, POINTER(MPVRenderParam))
i_vp_nd_nd = CFUNCTYPE(c_int, c_void_p, MPVNode, MPVNode)
i_vp_cpp_nd = CFUNCTYPE(c_int, c_void_p, POINTER(c_char_p), MPVNode)
i_vp_ui64_cpp = CFUNCTYPE(c_int, c_void_p, c_uint64, POINTER(c_char_p))
i_vp_ui64_nd = CFUNCTYPE(c_int, c_void_p, c_uint64, MPVNode)
i_vp_ui64_cp_vp = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_void_p)
i_vp_ui64_cp_i_vp = CFUNCTYPE(c_int, c_void_p, c_uint64, c_char_p, c_int, c_void_p)
i_vpp_vp_vp = CFUNCTYPE(c_int, POINTER(c_void_p), c_void_p, c_void_p)
i_vpp_vp_rpp = CFUNCTYPE(c_int, POINTER(c_void_p), c_void_p, POINTER(MPVRenderParam))
i64_vp = CFUNCTYPE(c_int64, c_void_p)
ul = CFUNCTYPE(c_ulong)
ui64_vp = CFUNCTYPE(c_int64, c_void_p)
vp = CFUNCTYPE(c_void_p)
vp_vp = CFUNCTYPE(c_void_p, c_void_p)
v_nd = CFUNCTYPE(None, MPVNode)
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
set_opt_p = get_opt_p + dat
get_opt = get_opt_p + ((1, "format"), (1, "data"))
set_opt = get_opt_p + ((1, "format"),) + dat
get_opt_a = con_tx + ((1, "reply_data"), (1, "name"), (1, "format"))
set_opt_a = get_opt_a + dat

ob_opt = get_opt_a
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
cts = con_tx + ((1, "param"),)
csc = con_tx + ((1, "callback"), (1, "callback_ctx"),)

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
free_node_contents = v_nd(("mpv_free_node_contents", mpv), nd)

# noinspection PyArgumentList
set_option = i_vp_cp_i_vp(("mpv_set_option", mpv), so)
# noinspection PyArgumentList
set_option_string = i_vp_cp_cp(("mpv_set_option_string", mpv), set_opt_p)

# noinspection PyArgumentList
command = i_vp_cpp(("mpv_command", mpv), cmd_p)
# noinspection PyArgumentList
command_node = i_vp_nd_nd(("mpv_command_node", mpv), cm_nd)
# noinspection PyArgumentList
command_ret = i_vp_cpp_nd(("mpv_command_ret", mpv), cm_nd)
# noinspection PyArgumentList
command_string = i_vp_cp(("mpv_command_string", mpv), cmd_p)
# noinspection PyArgumentList
command_async = i_vp_ui64_cpp(("mpv_command_async", mpv), cm_as)
# noinspection PyArgumentList
command_node_async = i_vp_ui64_nd(("mpv_command_node_async", mpv), cm_as)
# noinspection PyArgumentList
abort_async_command = v_vp_ui64(("mpv_abort_async_command", mpv), ab_cm)

# noinspection PyArgumentList
set_property = i_vp_cp_i_vp(("mpv_set_property", mpv), set_opt)
# noinspection PyArgumentList
set_property_string = i_vp_cp_cp(("mpv_set_property_string", mpv), set_opt_p)
# noinspection PyArgumentList
set_property_async = i_vp_ui64_cp_i_vp(("mpv_set_property_async", mpv), set_opt_a)
# noinspection PyArgumentList
get_property = i_vp_cp_i_vp(("mpv_get_property", mpv), get_opt)
# noinspection PyArgumentList
get_property_string = cp_vp_cp(("mpv_get_property_string", mpv), get_opt_p)
# noinspection PyArgumentList
get_property_osd_string = cp_vp_cp(("mpv_get_property_osd_string", mpv), get_opt_p)
# noinspection PyArgumentList
get_property_async = i_vp_ui64_cp_vp(("mpv_get_property_async", mpv), get_opt_a)
# noinspection PyArgumentList
observe_property = i_vp_ui64_cp_i(("mpv_observe_property", mpv), ob_opt)
# noinspection PyArgumentList, SpellCheckingInspection
unobserve_property = i_vp_ui64(("mpv_unobserve_property", mpv), u_ob_opt)

# noinspection PyArgumentList
event_name = cp_i(("mpv_event_name", mpv), ev)
# noinspection PyArgumentList
event_to_node = i_nd_ev(("mpv_event_to_node", mpv), en)
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
render_context_create = i_vpp_vp_rpp(("mpv_render_context_create", mpv), ctc)
# noinspection PyArgumentList
render_context_set_parameter = i_vp_rp(("mpv_render_context_set_parameter", mpv), cts)
# noinspection PyArgumentList
render_context_get_info = i_vp_rp(("mpv_render_context_get_info", mpv), cts)
# noinspection PyArgumentList
render_context_set_update_callback = v_vp_f_vp(("mpv_render_context_set_update_callback", mpv), csc)
# noinspection PyArgumentList
render_context_update = ui64_vp(("mpv_render_context_update", mpv), con_tx)
# noinspection PyArgumentList
render_context_render = i_vp_rpp(("mpv_render_context_render", mpv), cts)
# noinspection PyArgumentList
render_context_report_swap = v_vp(("mpv_render_context_report_swap", mpv), con_tx)
# noinspection PyArgumentList
render_context_free = v_vp(("mpv_render_context_free", mpv), con_tx)

# noinspection SpellCheckingInspection
__all__ = ["MPVEventStartFile", "MPVEventEndFile", "MPVEventClientMessage", "MPVEventHook", "MPVEventLogMessage", "MPVEventProperty", "MPVEvent",
           "MPVByteArray", "MPVUnion", "MPVNode", "MPVNodeList", "MPVEventCommand", "MPVRenderFrameInfo", "MPVRenderParam", "MPVError", "MPVFormat",
           "MPVEventId", "MPVLog", "MPVEndFileReason", "MPVRenderParamType", "MPVRenderFrameInfoFlags", "MPVRenderUpdateFlag", "client_api_version",
           "error_string", "free", "client_name", "client_id", "create", "initialize", "destroy", "terminate_destroy", "create_client",
           "create_weak_client", "load_config_file", "get_time_us", "free_node_contents", "set_option", "set_option_string", "command",
           "command_node", "command_ret", "command_string", "command_async", "command_node_async", "abort_async_command", "set_property",
           "set_property_string", "set_property_async", "get_property", "get_property_string", "get_property_osd_string", "get_property_async",
           "observe_property", "unobserve_property", "event_name", "event_to_node", "request_event", "request_log_messages", "wait_event", "wakeup",
           "set_wakeup_callback", "wait_async_requests", "hook_add", "hook_continue", "render_context_create", "render_context_set_parameter",
           "render_context_get_info", "render_context_set_update_callback", "render_context_update", "render_context_render",
           "render_context_report_swap", "render_context_free"]
