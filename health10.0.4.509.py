#-*-coding:utf-8-*-
import frida,sys
sys.path_hooks
def print_result(message):
    print ("[*] %s" % (message))

def on_message(message, data):
    type = message["type"]
    msg = message
    if type == "send":
        print_result(message["payload"])
    elif type == 'error':
        print(message['stack'])
    else:
        print(msg)

test = """
JSON.stringify()
    var objDisplayMetrics = Resources.getSystem().getDisplayMetrics();
    send(objDisplayMetrics.toString());
    var ByteString = Java.use("com.android.okhttp.okio.ByteString");
    ByteString.of(result).hex(); 
"""

jscode = """
setImmediate(function() {
Java.perform(function() {
    var Thread = Java.use("java.lang.Thread");
    var StackTrace = function(tag) {
        send(tag + "\\n" + Thread.currentThread().getStackTrace().toString());
    }
    var ByteString = Java.use("com.android.okhttp.okio.ByteString");
    
    
    var SQLiteDatabase = Java.use("net.sqlcipher.database.SQLiteDatabase");
    SQLiteDatabase.getBytes.implementation = function(cArr) {
        var ret = this.getBytes(cArr);
        send("SQLiteDatabase.getBytes()" + ByteString.of(ret).hex());
        return ret;
    }
    var KeyManager = Java.use("o.dlf");
    var key14 = KeyManager.d(14);
    send("key14:" + ByteString.of(key14).hex());
    
    var BaseApplication = Java.use("com.huawei.hwcommonmodel.application.BaseApplication");
    var context = BaseApplication.getContext();
    var cok = Java.use("o.cok");
    var objcok = cok.b(context);
    send("cok.b=" + cok.b.value);
    var db = objcok.c();
    send("getPageSize:" + db.getPageSize());
    send("getPath:" + db.getPath());
    
    var SQLiteOpenHelper = Java.use("net.sqlcipher.database.SQLiteOpenHelper");
    SQLiteOpenHelper.getWritableDatabase.overload('[C').implementation = function(cArr) {
        var ret = this.getWritableDatabase(cArr);
        var bytes = db.getBytes(cArr);
        send("getWritableDatabase(" + ByteString.of(bytes).hex() + ")");
        return ret;
    }
    objcok.getWritableDatabase(cok.g.value);
    
    send("Hook end!");
});
});
"""


process = frida.get_device("TEV0217405004733").attach("com.huawei.health")
#device = frida.get_usb_device()
#pid = device.spawn(["com.wniu.zufang"])
#process = device.attach(pid)
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
#device.resume(pid)
#process.detach()
sys.stdin.read()





















