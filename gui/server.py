from bottle import Bottle, run, template
import os

app = Bottle()

@app.route('/')
def index():
    by_id_dir = '/dev/input/by-id'
    devices = []
    for linkdfile in os.listdir(by_id_dir):
        if linkdfile:
            # twodots, dstname = os.path.split(os.readlink(os.path.join(by_id_dir, linkdfile)))
            # TODO: filter 
            devices.append(linkdfile)
    device_datas = []
    for dev_id in devices:
        name = dev_id
        reg = False
        
        style = 'padding:10px'
        if reg:
            style += ";color:red"
        
        device_datas.append({'name': name, 'reg': reg, 'style': style})
        
    tpl = '''<html>
    <body>
    <table border=1 align=center>
    <thead>

        <th>Device ID</th>
        <th>Registered</th>
        <th>ON/OFF</th>
        <th>WRAPPING KEY</th>
    </thead>
% for device in device_datas:
    <tr>
        <td style="{{device['style']}}"> {{ device['name'] }} </td>
        <td><select>
                <option value="yes" {{"selected" if device['reg'] else "" }}>YES</option>
                <option value="no" {{"selected" if not device['reg'] else "" }}>NO</option>
            </select>
        </td>
        <td><select>
                <option value="on">ON</option>
                <option value="off">OFF</option>
            </select>
        </td>
        <td><select>
                <option value="f20">F20</option>
                <option value="f21">F21</option>
                <option value="f22">F22</option>
                <option value="f23">F23</option>
            </select>
        </td>
    </tr>
% end
    </table>
    </body></html>'''
    return template(tpl, device_datas=device_datas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=True)