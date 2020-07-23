from code import interact
from ctypes import cdll, c_void_p, c_char_p, c_int64, c_int, c_long, POINTER

if __name__ == '__main__':
    mpv = cdll.LoadLibrary("D:/Depends/mpv/mpv-1.dll")
    mpv.mpv_client_api_version.restype = c_long
    mpv.mpv_initialize.argtypes = [c_void_p]
    mpv.mpv_create.restype = c_void_p
    mpv.mpv_create_client.argtypes = [c_void_p, c_char_p]
    mpv.mpv_create_client.restype = c_void_p
    mpv.mpv_create_weak_client.argtypes = [c_void_p, c_char_p]
    mpv.mpv_create_weak_client.restype = c_void_p

    mpv.mpv_client_name.argtypes = [c_void_p]
    mpv.mpv_client_name.restype = c_char_p
    mpv.mpv_client_id.argtypes = [c_void_p]
    mpv.mpv_client_id.restype = c_int64

    mpv.mpv_terminate_destroy.argtypes = [c_void_p]
    mpv.mpv_destroy.argtypes = [c_void_p]
    mpv.mpv_free.argtypes = [c_void_p]

    mpv.mpv_error_string.argtypes = [c_int]
    mpv.mpv_error_string.restype = c_char_p

    mpv.mpv_set_option_string.argtypes = [c_void_p, c_char_p, c_char_p]
    mpv.mpv_load_config_file.argtypes = [c_void_p, c_char_p]
    mpv.mpv_get_time_us.argtypes = [c_void_p]
    mpv.mpv_get_time_us.restype = c_int64

    mpv.mpv_command.argtypes = [c_void_p, POINTER(c_char_p)]
    mpv.mpv_command_string.argtypes = [c_void_p, c_char_p]

    mpv.mpv_set_property_string.argtypes = [c_void_p, c_char_p, c_char_p]
    mpv.mpv_get_property_string.argtypes = [c_void_p, c_char_p]
    mpv.mpv_get_property_string.restype = c_char_p

    mpv.mpv_get_property_osd_string.argtypes = [c_void_p, c_char_p]
    mpv.mpv_get_property_osd_string.restype = c_char_p

    mpv_handle = mpv.mpv_create()
    mpv.mpv_initialize(mpv_handle)

    # mpv.mpv_set_option_string(mpv_handle, c_char_p(b"audio-display"), c_char_p(b"yes"))

    # mpv_client_handle = mpv.mpv_create_client(mpv_handle, c_char_p(b"Worker"))

    # client_name = mpv.mpv_client_name(mpv_client_handle)
    # client_id = mpv.mpv_client_id(mpv_client_handle)

    client_name = mpv.mpv_client_name(mpv_handle)
    client_id = mpv.mpv_client_id(mpv_handle)

    print(client_name)
    print(client_id)

    mpv.mpv_command(mpv_handle, (c_char_p * 2)(c_char_p(b"loadfile"), c_char_p(b"ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr")))

    interact(banner="Mpv Player", local=locals(), exitmsg="Exit")

    mpv.mpv_command(mpv_handle, (c_char_p * 1)(c_char_p(b"quit")))

    # mpv.mpv_destroy(mpv_handle)

    mpv.mpv_terminate_destroy(mpv_handle)

    # mpv.mpv_free(mpv_handle)
