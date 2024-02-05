import keyboard
import os
import sys

all_devices = {}  # reset only by restart

NULL_CHAR = chr(0)

# https://source.android.com/devices/input/keyboard-devices
HID_Keyname_Usage = {
    'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08, 'f': 0x09, 'g': 0x0a, 'h': 0x0b, 'i': 0x0c, 'j': 0x0d, 
    'k': 0x0e, 'l': 0x0f, 'm': 0x10, 'n': 0x11, 'o': 0x12, 'p': 0x13, 'q': 0x14, 'r': 0x15, 's': 0x16, 't': 0x17, 
    'u': 0x18, 'v': 0x19, 'w': 0x1a, 'x': 0x1b, 'y': 0x1c, 'z': 0x1d, 
    
    '1': 0x1e, '2': 0x1f, '3': 0x20, '4': 0x21, '5': 0x22, '6': 0x23, '7': 0x24, '8': 0x25, '9': 0x26, '0': 0x27, 
    '!': 0x1e, '@': 0x00, '#': 0x00, '$': 0x00, '%': 0x00, '^': 0x00, '&': 0x00, '*': 0x00, '(': 0x00, ')': 0x00, 
    
    '-': 0x2d, '=': 0x2e, 
    '_': 0x2d, '+': 0x2e, 
    
    'enter': 0x28, 'esc': 0x29,
    
    'f1': 0x3a, 'f2': 0x3b  
}

# TODO: config file 
HID_device_wrapper_char = {
    'usb-Cypress_USB_Keyboard-event-kbd': 0x72,
    'usb-SONiX_USB_Keyboard-event-kbd': 0x73,

    'usb-test-event-kbd': 0x71
}

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def get_devicename(device):
    path, srcname = os.path.split(device)  # ('/dev/input', 'event0')
    by_id_dir = '/dev/input/by-id'
    for linkdfile in os.listdir(by_id_dir):
        if linkdfile:
            twodots, dstname = os.path.split(os.readlink(os.path.join(by_id_dir, linkdfile)))
            if srcname == dstname:
                return linkdfile  # string

def wrap_intercept(device_name, keyvalue):
    report1 = NULL_CHAR * 2 + chr(HID_device_wrapper_char[device_name]) + NULL_CHAR * 5
    report2 = NULL_CHAR * 2 + chr(HID_device_wrapper_char[device_name]) + chr(keyvalue) + NULL_CHAR * 4
    report3 = NULL_CHAR * 8

    return [report2, report3]
    # return [report1, report2, report3]

def print_pressed_keys(e):
    # {"is_keypad": false, "time": 1544415629.061856, "scan_code": 30, "event_type": "up", "device": "/dev/input/event0", "name": "a"}
    if e.device not in all_devices:
        all_devices[e.device] = {'name': get_devicename(e.device)}
        print('added Device:', all_devices)
    if e.event_type == 'up':
        for report_content in wrap_intercept(all_devices[e.device]['name'], HID_Keyname_Usage[e.name.lower()]):
            write_report(report_content)
            
def main():
    keyboard.hook(print_pressed_keys)
    keyboard.wait()

def test(method):
    for keyname in 'Hello_World_12345':
        print(keyname, keyname.lower(), HID_Keyname_Usage[keyname.lower()])
        for report in wrap_intercept('usb-test-event-kbd', HID_Keyname_Usage[keyname.lower()]):
            print('  ', end='')
            res = ''
            for b in report.encode():
                res += '%02x ' % b
            print(res)
            # print(type(report))
            if method != 'output_only':
                write_report(report)

# 컴퓨터\HKEY_LOCAL_MACHINE\SYSTEM\DriverDatabase\DriverPackages\input.inf_amd64_b9ba2bc564b0f008\Strings

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            test(method='')
        elif sys.argv[1] == 'test_output_only':
            test(method='output_only')
    else:
        main()
