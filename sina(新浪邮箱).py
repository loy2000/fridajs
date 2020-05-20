import frida
import sys


jscode = """

Java.perform(function() {
	send("oncreate")
	var ByteString = Java.use("com.android.okhttp.okio.ByteString");
    var Thread = Java.use("java.lang.Thread");
    var StackTrace = function(tag) {
        send(tag + "\\n" + Thread.currentThread().getStackTrace().toString());
    }

	   var application = Java.use("android.app.Application");
 
        application.attach.overload('android.content.Context').implementation = function(context) {
            var result = this.attach(context); // 先执行原来的attach方法
            var classloader = context.getClassLoader(); // 获取classloader
            Java.classFactory.loader = classloader;
            var SQLiteOpenHelper = Java.classFactory.use("net.sqlcipher.database.SQLiteOpenHelper"); //这里不能直接使用Java.use，因为java.use会检查在不在perform里面，不在就会失败
            console.log("SQLiteOpenHelper: " + SQLiteOpenHelper);
            // 然后下面的代码就和写正常的hook一样啦
            SQLiteOpenHelper.getWritableDatabase.overload('java.lang.String').implementation = function(a) {
                send("dbkey" + a);	
                return this.getWritableDatabase(a);
            }
            return result;
        }
	var SQLiteDatabase = Java.use("net.sqlcipher.database.SQLiteDatabase");
	var SQLiteOpenHelper = Java.use("net.sqlcipher.database.SQLiteOpenHelper");
	 SQLiteOpenHelper.getWritableDatabase.overload('java.lang.String').implementation = function(a) {
                send("dbkey" + a);	
                return this.getWritableDatabase(a);
            }
	SQLiteOpenHelper.getReadableDatabase.overload('java.lang.String').implementation = function(a) {
                send("dbkey" + a);	
                return this.getReadableDatabase(a);
            }
	SQLiteDatabase.loadLibs.overload('android.content.Context', 'java.io.File', 'net.sqlcipher.database.SQLiteDatabase$LibraryLoader').implementation  = function(a,b,c) {
        send("oncreate11")
		
        return this.loadLibs(a,b,c);
    }
	var mySystem = Java.use("java.lang.System")
	mySystem.loadLibrary.overload('java.lang.String').implementation = function(a) {
                send("lib=" + a);	
                return this.loadLibrary(a);
            }

	/*
	SQLiteOpenHelper.$init.overload('android.content.Context', 'java.lang.String', '[B', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler').implementation  = function(a,b,c,d,e) {
        send("oncreate13")
		if(c != null)
		{
			send("password" + ByteString.of(c).hex());
		}
        send("db" + b);		
        return this.$init(a,b,c,d,e);
    }
	var SampleDriverFactory = Java.use("com.tencent.melonteam.framework.chat.msgchannel.hmscore.IMHMSConfig$SampleDriverFactory");
    SampleDriverFactory.createSqlDriver.implementation = function(a,b) {
        send("oncreate2")
        return this.createSqlDriver(a,b);
		
    }
	var MLog = Java.use("com.tencent.melonteam.log.MLog");
    MLog.i.overload('java.lang.String', 'java.lang.String').implementation = function(a,b) {
        //send("tag="+a+"msg="+b);
        return this.i(a,b);
		
    }
    var SQLiteDatabase = Java.use("com.tencent.wcdb.database.SQLiteDatabase");
    SQLiteDatabase.openDatabase.overload('java.lang.String', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int').implementation = function(a,b,c) {
        send("oncreate2")
		send("db" + a);		
        return this.openDatabase(a,b,c);
		
    }
	 SQLiteDatabase.openDatabase.overload('java.lang.String', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler').implementation = function(a,b,c,d) {
        send("oncreate3")
		send("db" + a);		
        return this.openDatabase(a,b,c,d);
		
    }
	 SQLiteDatabase.openDatabase.overload('java.lang.String', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler', 'int').implementation = function(a,b,c,d,e) {
        send("oncreate3")
		send("db" + a);		
        return this.openDatabase(a,b,c,d,e);
		
    }
	SQLiteDatabase.openDatabase.overload('java.lang.String', '[B', 'com.tencent.wcdb.database.SQLiteCipherSpec', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler').implementation = function(a,b,c,d,e,f) {
        send("oncreate3")
		send("db" + a);		
        return this.openDatabase(a,b,c,d,e,f);
		
    }
	SQLiteDatabase.openDatabase.overload('java.lang.String', '[B', 'com.tencent.wcdb.database.SQLiteCipherSpec', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler', 'int').implementation = function(a,b,c,d,e,f,g) {
        send("oncreate3")
		send("db" + a);		
        return this.openDatabase(a,b,c,d,e,f,g);
		
    }
	 var DatabaseModule = Java.use("com.tencent.melonteam.database.DatabaseModule");
    DatabaseModule.openDatabase.overload('java.lang.String', 'com.tencent.melonteam.idl.database.OpenDBConfig', 'com.tencent.melonteam.idl.database.IDBCallback').implementation = function(a,b,c) {
        send("oncreate2")
		send("db" + a);		
        return this.openDatabase(a,b,c);
		
    }*/

        Interceptor.attach(Module.findExportByName("libJNIEncrypt.so" , "getCode"), {
        onEnter: function (args) {
            
            //send("key:\\n" + hexdump(args[0], {offset: 0,length: 72, header: true, ansi: true}));
            
        },
        onLeave: function (retval) {
		send("key:\\n"+(retval.toString()).hex())
        }
		});
		var AESEncrypt =  Java.use("com.sina.mail.AESEncrypt");
		var App = Java.use("com.sina.mail.MailApp");
		var key = AESEncrypt.getCode(App.u());
		send("key="+key);
	
});
"""




def on_message(message, data):
	type = message["type"]
	msg = message
	if type == "send":
		msg = message["payload"]
	elif type == 'error':
		msg = message['stack']	
		
	print(msg)		
def main(apk):
    
   device = frida.get_usb_device(10)
   pid = device.spawn(apk)
   process = device.attach(pid)
   device.resume(pid)
   script = process.create_script(jscode)
   script.on('message', on_message)
   script.load()
   sys.stdin.read()
	

if __name__ == '__main__':
    index = 0
    main("com.sina.mail.free")
    sys.exit(0)